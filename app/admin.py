from django.contrib import admin
from .models import Reporte, Garantia

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre', 'apellidos', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'numero_reporte')
    search_fields = ('vin', 'nombre', 'apellidos', 'email', 'telefono')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

@admin.register(Garantia)
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
