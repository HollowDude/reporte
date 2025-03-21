from django import forms
from django.contrib import admin
from .models import registro, garantia, cliente, empresa, triciclo, power_station
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin



class MiAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Define el orden deseado de las aplicaciones y modelos
        orden_aplicaciones = [
            {'name': 'Registro', 'models': [
                {'name': 'Registro', 'admin_url': '/admin/app/registro'},
                {'name': 'Garantia', 'admin_url': '/admin/app/garantia/'},
            ]},
            {'name': 'Cliente', 'models': [
                {'name': 'Cliente', 'admin_url': '/admin/app/cliente/'},
            ]},
            {'name': 'Empresa', 'models': [
                {'name': 'Empresa', 'admin_url': '/admin/app/empresa/'},
            ]},
            {'name': 'Triciclo', 'models': [
                {'name': 'Triciclo', 'admin_url': '/admin/app/triciclo/'},
            ]},
            {'name': 'Power Station', 'models': [
                {'name': 'Power Station', 'admin_url': '/admin/app/power_station/'},
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
    class Meta:
        model = registro.Registro
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación comprador
        if bool(cleaned_data.get('cliente')) == bool(cleaned_data.get('empresa')):
            raise forms.ValidationError("Selecciona solo un Cliente o una Empresa")
            
        # Validación producto
        if bool(cleaned_data.get('triciclo')) == bool(cleaned_data.get('power_station')):
            raise forms.ValidationError("Selecciona solo un Triciclo o una Power Station")
            
        return cleaned_data

class GarantiaForm(forms.ModelForm):
    class Meta:
        model = garantia.Garantia
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        
        # Validación comprador
        if bool(cleaned_data.get('cliente')) == bool(cleaned_data.get('empresa')):
            raise forms.ValidationError("Selecciona solo un Cliente o una Empresa")
            
        # Validación producto
        if bool(cleaned_data.get('triciclo')) == bool(cleaned_data.get('power_station')):
            raise forms.ValidationError("Selecciona solo un Triciclo o una Power Station")
            
        return cleaned_data


@admin.register(cliente.Cliente, site=mi_admin_site)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'carnet', 'direccion', 'email', 'telefono')

@admin.register(empresa.Empresa, site=mi_admin_site)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nit', 'direccion', 'email', 'telefono')

@admin.register(triciclo.Triciclo, site=mi_admin_site)
class TricicloAdmin(admin.ModelAdmin):
    list_display = ["vin", "fecha_armado", "num_m", "extensor_rango", "sello", "fecha_autorizado", "autorizado"]
    search_fields = ('autorizado', 'fecha_autorizado')

@admin.register(power_station.Power_Station, site=mi_admin_site)
class PowerAdmin(admin.ModelAdmin):
    list_display = ["sn", "fecha_armado"]


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
            'fields': ('fecha_entregado', 'llamada', 'numero_reporte', 'tiempoR'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if not obj:  # Creando
            readonly_fields.extend(['llamada'])
        else:  # Editando
            if obj.llamada:
                readonly_fields.append('llamada')
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
        }),
        ('Otros', {
            'fields': ('motivo', 'evaluacion', 'trabajos_hechos', 'piezas_usadas', 'recomendaciones', 'nombre_especialista', 'conformidad_cliente', 'facturar_a',),
        })
    )


