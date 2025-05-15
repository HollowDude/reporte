from django import forms
from django.contrib import admin
from .models import registro, registro_ps, garantia, cliente, empresa, triciclo, power_station, panels, garantia_p
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.db import models
from django.forms.models import BaseInlineFormSet
from django.db.models import Q



class MiAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        orden_aplicaciones = [
            {'name': 'Registros', 'models': [
                {'name': 'Relacion de ventas(Triciclos)', 'admin_url': '/admin/app/registro'},
                {'name': 'Relacion de ventas(Power Stations)', 'admin_url': '/admin/app/registro_ps'},
                {'name': 'Reporte de Reclamaciones(Triciclos)', 'admin_url': '/admin/app/garantia/'},
                {'name': 'Reporte de Reclamaciones(Power Stations)', 'admin_url': '/admin/app/garantia_p/'},
            ]},
            {'name': 'Clientes Unificados', 'models': [
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

REGISTRO_CHOICES_SIN_TODOS = [
    choice for choice in registro.Registro.RECEPTOR_CHOICES if choice[0] != 'sales07@fuetasa.com'
]

class RegistroForm(forms.ModelForm):
    receptor = forms.MultipleChoiceField(
        choices=REGISTRO_CHOICES_SIN_TODOS,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = registro.Registro
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instancia = getattr(self, 'instance', None)

        # 1) Queremos todos los no vendidos + el que ya está asignado
        if instancia and instancia.pk and instancia.triciclo:
            qs = triciclo.Triciclo.objects.filter(
                Q(vendido=False) | Q(pk=instancia.triciclo.pk)
            )
        else:
            qs = triciclo.Triciclo.objects.filter(vendido=False)

        # 2) Excluimos los VINs usados en otros registros
        if instancia and instancia.pk:
            usados = registro.Registro.objects.exclude(pk=instancia.pk) \
                        .filter(triciclo__isnull=False) \
                        .values_list('triciclo__vin', flat=True)
            qs = qs.exclude(vin__in=usados)

        self.fields['triciclo'].queryset = qs

    def clean_receptor(self):
        data = self.cleaned_data['receptor']
        return ','.join(data)

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        empresa = cleaned_data.get('empresa')
        if (cliente and empresa) or (not cliente and not empresa):
            raise forms.ValidationError("Selecciona solo un Cliente o una Empresa")
        return cleaned_data

class Registro_psForm(forms.ModelForm):
    receptor = forms.MultipleChoiceField(
        choices=REGISTRO_CHOICES_SIN_TODOS,
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    
    class Meta:
        model = registro_ps.Registro_ps
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instancia = getattr(self, 'instance', None)

        # 1) Todos los no vendidos + la propia asignada
        if instancia and instancia.pk and instancia.power_station:
            qs = power_station.Power_Station.objects.filter(
                Q(vendido=False) | Q(pk=instancia.power_station.pk)
            )
        else:
            qs = power_station.Power_Station.objects.filter(vendido=False)

        # 2) Excluir las PS usadas en otros registros
        if instancia and instancia.pk:
            usados = (
                registro_ps.Registro_ps.objects
                    .exclude(pk=instancia.pk)
                    .filter(power_station__isnull=False)
                    .values_list('power_station__sn', flat=True)
            )
            qs = qs.exclude(sn__in=usados)

        self.fields['power_station'].queryset = qs.distinct()
        self.fields['power_station'].to_field_name = 'sn'

    def clean_receptor(self):
        data = self.cleaned_data['receptor']
        return ','.join(data)

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        empresa = cleaned_data.get('empresa')
        if (cliente and empresa) or (not cliente and not empresa):
            raise forms.ValidationError("Selecciona solo un Cliente o una Empresa")
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
    list_display = ('kit', 'aut', 'cuchilla', 'act', 'num')

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
    readonly_fields = ["fecha_v", "vendido"]
    list_display = ["vin", "modelo", "fecha_armado", "num_m", "extensor_rango", "sello", "fecha_autorizado", "autorizado", "obser", "vendido", "fecha_v"]
    search_fields = ('autorizado', 'fecha_autorizado')

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))

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
            '300w': 1,
            '600w': 1,
            '1200w': 2,
            '2400w': 3,
            '3000w': 3,
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
    fk_name = 'power_station'  

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
    readonly_fields = ["w", "paneles", "expansiones", "bases", "vendido", "fecha_v"]
    fields = ["sn",  "modelo", "marca", "dist", "tipo", "fecha_armado", "w", "paneles", "expansiones", "bases", "vendido", "fecha_v"]
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
            'fields': (('triciclo'),),
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

        if not obj or obj.llamada:
            readonly_fields.extend(['llamada', 'receptor'])
        
        return readonly_fields



    
    @admin.register(registro_ps.Registro_ps, site=mi_admin_site)
    class Registro_psAdmin(admin.ModelAdmin):
        form = Registro_psForm
        readonly_fields = ['numero_reporte', 'tiempoR', 'tiempoR_pan']
        fieldsets = (
            ('Comprador', {
                'fields': (('cliente', 'empresa'),),
            }),
            ('Producto', {
                'fields': (('power_station'),),
            }),
            ('Otros', {
                'fields': ('fecha_entregado', 'numero_reporte', 'tiempoR', 'tiempoR_pan'),
            }),
            ('Notificación', {
                'fields': ('llamada', 'receptor'),
            }),
        )

        def get_readonly_fields(self, request, obj=None):
            readonly_fields = list(super().get_readonly_fields(request, obj))

            if not obj or obj.llamada:
                readonly_fields.extend(['llamada', 'receptor'])
            
            return readonly_fields

    


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
    
 

@admin.register(garantia_p.Garantia_P, site=mi_admin_site)
class GarantiaAdmin(admin.ModelAdmin):
    readonly_fields = ['num']
    fieldsets = (
        ('Remitente', {
            'fields': (('cliente', 'empresa'),),
            'description': "Seleccione SOLO UN Cliente o una Empresa"
        }),
        ('Producto', {
            'fields': ('power_station',),
            'description': "Power Stations vendidas al cliente/empresa (seleccione primero cliente/empresa y guarde)"
        }),
        ('Datos de Garantía', {
            'fields': ('num', 'fecha_em'),
            'description': "Información básica de la garantía"
        }),
        ('Condiciones Generales', {
            'fields': ('condiciones_generales',),
            'classes': ('collapse',),
            'description': "Términos básicos de la garantía"
        }),
        ('Exclusiones de Garantía', {
            'fields': ('exclusiones_garantia',),
            'classes': ('collapse',),
            'description': "Situaciones no cubiertas por la garantía"
        }),
        ('Políticas de Reparación', {
            'fields': ('condiciones_reparacion',),
            'classes': ('collapse',),
            'description': "Procedimientos para reparaciones cubiertas"
        }),
        ('Políticas de Sustitución', {
            'fields': ('condiciones_sustitucion',),
            'classes': ('collapse',),
            'description': "Condiciones para reemplazo del producto"
        }),
        ('Costos y Coberturas', {
            'fields': ('politicas_costos',),
            'classes': ('collapse',),
            'description': "Detalles de costos asociados"
        }),
        ('Procedimiento de Reclamo', {
            'fields': ('procedimiento_reclamo',),
            'description': "Pasos para hacer válida la garantía"
        })
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not obj:  # Si es creación
            return list(readonly_fields) + ['power_station']
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "power_station":
            object_id = request.resolver_match.kwargs.get('object_id')
            if object_id:
                obj = self.get_object(request, object_id)
                if obj:
                    # Determinar si es cliente o empresa
                    if obj.cliente:
                        registros = registro_ps.Registro_ps.objects.filter(cliente=obj.cliente, power_station__isnull=False)
                    elif obj.empresa:
                        registros = registro_ps.Registro_ps.objects.filter(empresa=obj.empresa, power_station__isnull=False)
                    else:
                        registros = registro_ps.Registro_ps.objects.none()

                    ps_sns = registros.values_list('power_station__sn', flat=True)
                    kwargs["queryset"] = power_station.Power_Station.objects.filter(sn__in=ps_sns)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
        # Help texts contextuales
        if 'cliente' in form.base_fields:
            form.base_fields['cliente'].help_text = "Cliente particular registrado"
        if 'empresa' in form.base_fields:
            form.base_fields['empresa'].help_text = "Empresa registrada"
        if 'power_station' in form.base_fields:
            form.base_fields['power_station'].help_text = "Solo muestra Power Stations vendidas a este cliente/empresa"
        
        return form

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        empresa = cleaned_data.get('empresa')
        
        # Validación exclusividad cliente/empresa
        if bool(cliente) == bool(empresa):  # Ambos o ninguno
            raise forms.ValidationError(
                "Debe seleccionar exclusivamente un Cliente O una Empresa, no ambos ni dejar vacío."
            )
        
        return cleaned_data