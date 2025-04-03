from django import forms
from django.contrib import admin
from .models import registro, garantia, cliente, empresa, triciclo, power_station, panels
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.db import models
from django.forms.models import BaseInlineFormSet



class MiAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        orden_aplicaciones = [
            {'name': 'Registros', 'models': [
                {'name': 'Relacion de ventas', 'admin_url': '/admin/app/registro'},
                {'name': 'Reporte de Reclamaciones', 'admin_url': '/admin/app/garantia/'},
            ]},
            {'name': 'Clientes', 'models': [
                {'name': 'Registros de T.C.P/P.N', 'admin_url': '/admin/app/cliente/'},
                {'name': 'Registros de MIPYME', 'admin_url': '/admin/app/empresa/'},
            ]},
            {'name': 'Ventas', 'models': [
                {'name': 'Triciclos Armados', 'admin_url': '/admin/app/triciclo/'},
                {'name': 'Power Station', 'admin_url': '/admin/app/power_station/'},
                {'name': 'Paneles Solares', 'admin_url': '/admin/app/panels/'}
            ]},
            {'name': 'Autenticación y Autorización', 'models': [
                {'name': 'Usuarios', 'admin_url': '/admin/auth/user/'},
                {'name': 'Grupos', 'admin_url': '/admin/auth/group/'},
            ]},
        ]
        return orden_aplicaciones

mi_admin_site = MiAdminSite(name='miadmin')
mi_admin_site.site_header = 'Administración de Empresa'
mi_admin_site.site_title = 'Administracion'
mi_admin_site.index_title = 'Bienvenido al administrador de Empresa'
mi_admin_site.register(User, UserAdmin)
mi_admin_site.register(Group, GroupAdmin)


class RegistroForm(forms.ModelForm):
    receptor = forms.MultipleChoiceField(
        choices=registro.Registro.RECEPTOR_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta:
        model = registro.Registro
        fields = '__all__'

    def clean_receptor(self):
        data = self.cleaned_data['receptor']
        return ','.join(data)

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación comprador
        cliente = cleaned_data.get('cliente')
        empresa = cleaned_data.get('empresa')
        if (cliente and empresa) or (not cliente and not empresa):
            raise forms.ValidationError("Selecciona solo un Cliente o una Empresa")
            
        # Validación producto
        triciclo = cleaned_data.get('triciclo')
        power_station = cleaned_data.get('power_station')
        
        # Contar cuántos productos están seleccionados
        count = sum([bool(triciclo), bool(power_station)])
        
        if count > 1:
            raise forms.ValidationError("Selecciona solo un Triciclo o una Power Station")
        
        return cleaned_data

class GarantiaForm(forms.ModelForm):
    class Meta:
        model = garantia.Garantia
        fields = '__all__'
        help_texts = {
            'triciclo': 'Guarde primero después de seleccionar cliente/empresa.',
            'power_station': 'Guarde primero después de seleccionar cliente/empresa.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        
        # Si es creación (no tiene PK), deshabilitar campos de producto
        if not instance or not instance.pk:
            for field in ['triciclo', 'power_station']:
                if field in self.fields:  # ¡Verificar si el campo existe!
                    self.fields[field].disabled = True
                    self.fields[field].help_text = "Guarde primero después de seleccionar cliente/empresa."


@admin.register(cliente.Cliente, site=mi_admin_site)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'carnet', 'direccion', 'email', 'telefono')

@admin.register(panels.Panels, site=mi_admin_site)
class PanelsAdmin(admin.ModelAdmin):
    list_display = ('kit', 'aut', 'cuchilla', 'act')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Si está creando un registro
        if not obj:
            readonly_fields.extend(['aut'])
        
        return readonly_fields

@admin.register(empresa.Empresa, site=mi_admin_site)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'direccion', 'email', 'telefono')

@admin.register(triciclo.Triciclo, site=mi_admin_site)
class TricicloAdmin(admin.ModelAdmin):
    list_display = ["vin", "fecha_armado", "num_m", "extensor_rango", "sello", "fecha_autorizado", "autorizado"]
    search_fields = ('autorizado', 'fecha_autorizado')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Si está creando un registro
        if not obj:
            readonly_fields.extend(['autorizado']) 
        
        return readonly_fields




class PowerStationPanelInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        tipo = None
        if self.instance and self.instance.pk:
            tipo = self.instance.tipo
        else:
            tipo = self.data.get('tipo')  # Obtener tipo del formulario principal
        
        tipo_mapping = {
            '1-300w': 1,
            '2-600w': 1,
            '3-1200w': 2,
            '4-2400w': 3,
            '5-3000w': 3,
        }
        required = tipo_mapping.get(tipo, 0)
        
        count = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False) and form.cleaned_data.get('panel'):
                count += 1
        
        if count != required:
            raise forms.ValidationError(f"Se requieren {required} paneles para el tipo {tipo}.")

class PowerStationPanelInline(admin.TabularInline):
    model = power_station.PowerStationPanel
    formset = PowerStationPanelInlineFormset
    extra = 3  # Máximo necesario
    verbose_name = "Panel"
    verbose_name_plural = "Paneles"
    fk_name = 'power_station'  # Obligatorio si hay múltiples ForeignKeys al mismo modelo

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'panel':
            power_station_id = request.resolver_match.kwargs.get('object_id')
            linked_panels = power_station.PowerStationPanel.objects.exclude(
                power_station_id=power_station_id
            ).values_list('panel_id', flat=True)
            kwargs['queryset'] = panels.Panels.objects.exclude(id__in=linked_panels)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



@admin.register(power_station.Power_Station, site=mi_admin_site)
class PowerAdmin(admin.ModelAdmin):
    list_display = ["sn", "tipo", "w", "paneles", "expansiones", "bases", "fecha_armado"]
    readonly_fields = ["w", "paneles", "expansiones", "bases"]
    fields = ["sn", "tipo", "fecha_armado", "w", "paneles", "expansiones", "bases"]
    inlines = [PowerStationPanelInline]



@admin.register(registro.Registro, site=mi_admin_site)
class RegistroAdmin(admin.ModelAdmin):
    form = RegistroForm
    readonly_fields = ['numero_reporte', 'tiempoR']
    fieldsets = (
        ('Comprador', {
            'fields': (('cliente', 'empresa'),),
        }),
        ('Producto', {
            'fields': (('triciclo', 'power_station'),),
        }),
        ('Otros', {
            'fields': ('fecha_entregado', 'numero_reporte', 'tiempoR'),
        }),
        ('Notificación', {
            'fields': ('llamada', 'receptor'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        
        # Si está creando un registro
        if not obj or obj.llamada:
            readonly_fields.extend(['llamada', 'receptor'])  # Bloquear ambos campos
        
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj_id = request.resolver_match.kwargs.get('object_id')
        
        if db_field.name == "triciclo":
            excluded_vins = registro.Registro.objects.exclude(pk=obj_id) \
                                                    .exclude(triciclo__isnull=True) \
                                                    .values_list('triciclo__vin', flat=True)
            kwargs["queryset"] = triciclo.Triciclo.objects.exclude(vin__in=excluded_vins)

        elif db_field.name == "power_station":
            excluded_sns = registro.Registro.objects.exclude(pk=obj_id) \
                                                  .exclude(power_station__isnull=True) \
                                                  .values_list('power_station__sn', flat=True)
            kwargs["queryset"] = power_station.Power_Station.objects.exclude(sn__in=excluded_sns)


        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(garantia.Garantia, site=mi_admin_site)
class GarantiaAdmin(admin.ModelAdmin):
    form = GarantiaForm
    fieldsets = (
        ('Remitente', {
            'fields': (('cliente', 'empresa'),),
        }),
        ('Producto', {
            'fields': (('triciclo', 'power_station'),),
            'description': "Seleccione un producto después de guardar y elegir cliente/empresa."  # Texto descriptivo
        }),
        ('Otros', {
            'fields': ('motivo', 'evaluacion', 'trabajos_hechos', 'piezas_usadas', 'recomendaciones', 'nombre_especialista', 'conformidad_cliente'),
        })
    )

    def get_readonly_fields(self, request, obj=None):
        return super().get_readonly_fields(request, obj)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj_id = request.resolver_match.kwargs.get('object_id')
        if not obj_id:  # Si es creación, no filtrar
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        obj = self.get_object(request, obj_id)
        if not obj or not (obj.cliente or obj.empresa):
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # Obtener registros de venta del cliente/empresa
        registros = registro.Registro.objects.filter(
            models.Q(cliente=obj.cliente) | models.Q(empresa=obj.empresa)
        )

        # Filtrar productos según registros de venta
        if db_field.name == "triciclo":
            triciclos_ids = registros.exclude(triciclo__isnull=True).values_list('triciclo_id', flat=True)
            kwargs["queryset"] = triciclo.Triciclo.objects.filter(vin__in=triciclos_ids)
        elif db_field.name == "power_station":
            ps_ids = registros.exclude(power_station__isnull=True).values_list('power_station_id', flat=True)
            kwargs["queryset"] = power_station.Power_Station.objects.filter(sn__in=ps_ids)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)