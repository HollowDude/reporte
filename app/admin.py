from django import forms
from django.contrib import admin
from .models import Registro_Clientes, Garantia, Registro_Clientes_Pendientes, Registro_Empresa, Registro_Empresa_Pendientes

@admin.register(Registro_Clientes)
class Registro_ClientesAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre', 'apellidos', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'sello', 'numero_reporte', 'llamada')
    search_fields = ('vin', 'nombre', 'apellidos', 'email', 'telefono')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['llamada']
        return [] 

@admin.register(Registro_Clientes_Pendientes)
class Registro_Clientes_PendientesAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre', 'apellidos', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'sello', 'numero_reporte', 'autorizado')
    search_fields = ('vin', 'nombre', 'apellidos', 'email', 'telefono')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['autorizado']
        return [] 



@admin.register(Registro_Empresa)
class Registro_EmpresaAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre_empresa', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'sello', 'articulo', 'numero_reporte', 'llamada')
    search_fields = ('vin', 'nombre_empresa', 'email', 'telefono', 'articulo')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['llamada']
        return [] 




@admin.register(Registro_Empresa_Pendientes)
class Registro_Empresa_PendientesAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre_empresa', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'sello', 'articulo', 'numero_reporte', 'autorizado')
    search_fields = ('vin', 'nombre_empresa', 'email', 'telefono')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return ['autorizado']
        return [] 




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
