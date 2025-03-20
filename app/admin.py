from django import forms
from django.contrib import admin
from .models import registro, garantia, cliente, empresa, triciclo, power_station


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

@admin.register(cliente.Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellidos', 'carnet', 'direccion', 'email', 'telefono')

@admin.register(empresa.Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'email', 'telefono')

@admin.register(triciclo.Triciclo)
class TricicloAdmin(admin.ModelAdmin):
    list_display = ["vin", "fecha_armado", "num_m", "modelo"]

@admin.register(triciclo.Triciclo_Pendiente)
class TricicloPendienteAdmin(admin.ModelAdmin):
    list_display = ["vin", "fecha_armado", "modelo", "num_m", "autorizado"]

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['autorizado']
        return [] 

@admin.register(power_station.Power_Station)
class PowerAdmin(admin.ModelAdmin):
    list_display = ["sn", "fecha_armado"]


@admin.register(registro.Registro)
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
            'fields': ('fecha_entregado', 'extensor_rango', 'sello', 'llamada', 'numero_reporte', 'tiempoR'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = list(super().get_readonly_fields(request, obj))
        if obj: 
            readonly_fields.extend(['numero_reporte', 'tiempoR'])
        return readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj_id = request.resolver_match.kwargs.get('object_id')
        
        if db_field.name == "triciclo":
            # Excluir triciclos usados en otros registros (excepto el actual)
            excluded_vins = registro.Registro.objects.exclude(pk=obj_id) \
                                                    .exclude(triciclo__isnull=True) \
                                                    .values_list('triciclo__vin', flat=True)
            kwargs["queryset"] = triciclo.Triciclo.objects.exclude(vin__in=excluded_vins)

        elif db_field.name == "power_station":
            # Excluir power stations usadas en otros registros (excepto el actual)
            excluded_sns = registro.Registro.objects.exclude(pk=obj_id) \
                                                  .exclude(power_station__isnull=True) \
                                                  .values_list('power_station__sn', flat=True)
            kwargs["queryset"] = power_station.Power_Station.objects.exclude(sn__in=excluded_sns)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
@admin.register(registro.Registro_Pendiente)
class Registro_PendienteAdmin(admin.ModelAdmin):
    form = RegistroForm
    readonly_fields = ['numero_reporte']
    fieldsets = (
        ('Comprador', {
            'fields': (('cliente', 'empresa'),),
        }),
        ('Producto', {
            'fields': (('triciclo', 'power_station'),),
        }),
        ('Otros', {
            'fields': ('fecha_entregado', 'extensor_rango', 'sello', 'autorizado'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['autorizado']
        return [] 

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        obj_id = request.resolver_match.kwargs.get('object_id')
        
        if db_field.name == "triciclo":
            # Excluir triciclos usados en otros registros (excepto el actual)
            excluded_vins = registro.Registro.objects.exclude(pk=obj_id) \
                                                    .exclude(triciclo__isnull=True) \
                                                    .values_list('triciclo__vin', flat=True)
            kwargs["queryset"] = triciclo.Triciclo.objects.exclude(vin__in=excluded_vins)

        elif db_field.name == "power_station":
            # Excluir power stations usadas en otros registros (excepto el actual)
            excluded_sns = registro.Registro.objects.exclude(pk=obj_id) \
                                                  .exclude(power_station__isnull=True) \
                                                  .values_list('power_station__sn', flat=True)
            kwargs["queryset"] = power_station.Power_Station.objects.exclude(sn__in=excluded_sns)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(garantia.Garantia)
class GarantiaAdmin(admin.ModelAdmin):
    list_display = ('get_usuario_nombre_completo', 'get_usuario_dir', 'get_usuario_tell', 'vin', 'modelo', 'motor_num', 'fecha_fabr', 'peso', 'voltaje', 'potencia', 'motivo', 'evaluacion', 'trabajos_hechos', 'piezas_usadas', 'recomendaciones', 'nombre_especialista', 'conformidad_cliente', 'facturar_a')
    search_fields = ('get_usuario_nombre_completo', 'get_usuario_tell', 'evaluacion', 'nombre_especialista', 'facturar_a')
    ordering = ('-fecha_fabr',)

    @admin.display(empty_value="???")
    def get_usuario_nombre_completo(self, obj):
        return f"{obj.usuario.nombre} {obj.usuario.apellidos}"
    @admin.display(empty_value="???")
    def get_usuario_dir(self, obj):
        return f"{obj.usuario.direccion}"
    @admin.display(empty_value="???")
    def get_usuario_tell(self, obj):
        return f"{obj.usuario.telefono}"
    
    get_usuario_dir.short_description = "Usuario direccion"
    get_usuario_tell.short_description = "Usuario telefono"
    get_usuario_nombre_completo.short_description = 'Nombre del usuario' 


# Register your models here.
