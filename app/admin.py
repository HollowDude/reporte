from django.contrib import admin
from .models import Reporte

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('vin', 'nombre', 'apellidos', 'email', 'telefono', 'fecha_armado', 'fecha_entregado','extensor_rango', 'numero_reporte')
    search_fields = ('vin', 'nombre', 'apellidos', 'email', 'telefono')
    list_filter = ('fecha_armado', 'fecha_entregado')
    ordering = ('-numero_reporte',)

# Register your models here.
