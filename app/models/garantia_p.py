from datetime import date
from django.db import models
from django.dispatch import receiver
from .cliente import Cliente
from .empresa import Empresa
from .power_station import Power_Station
from django.db.models.signals import pre_save

class Garantia_P(models.Model):
    num = models.IntegerField("Numero de Garantia", primary_key=True, help_text="Se genera automaticamente y es secuencial")
    fecha_em = models.DateField("Fecha de Emision", default=date.today())
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL, help_text="Aca estaran los datos especificos de la Power Station y sus paneles asociados, acceder para ver detalles.")
    
    # Sección de condiciones generales
    condiciones_generales = models.TextField(
        "Condiciones Generales de Garantía",
        default="""- La estación de energía incluye una garantía de 1 año contra defectos de fabricación.
- El panel solar incluye una garantía de 2 años y cubre defectos de fabricación.
- La garantía del generador solar no cubre daños por uso inadecuado, accidentes o modificaciones no autorizadas.
- Si el producto se usa de manera incorrecta o no según las instrucciones del fabricante, la garantía no cubrirá los daños resultantes.""",
        help_text="Condiciones generales de la garantía por defecto"
    )
    
    # Sección de exclusiones de garantía
    exclusiones_garantia = models.TextField(
        "Exclusiones de la Garantía",
        default="""- Daños por uso incorrecto o negligencia.
- Modificaciones o reparaciones no autorizadas.
- Desgaste normal de la batería.
- Daños por factores externos (sobretensiones, rayos, inundaciones, etc.).
- Uso en condiciones extremas fuera de los rangos especificados.
- Falta de mantenimiento según instrucciones del fabricante.
- Consumibles o accesorios (cables, adaptadores).
- Daños por software no autorizado.
- Daños cosméticos (arañazos, abolladuras) que no afectan el funcionamiento.""",
        help_text="Lista de situaciones que no están cubiertas por la garantía"
    )
    
    # Sección de reparación
    condiciones_reparacion = models.TextField(
        "Condiciones de Reparación",
        default="""Cuando surjan problemas comunes como:
- Fallos en la batería (pérdida de capacidad, incapacidad de cargarse).
- Problemas con los puertos de salida (USB, CA, DC).
- Errores en la pantalla LCD o interfaz de usuario.
- Fallos en el sistema de gestión de energía (sobrecalentamiento, cortocircuitos).

El técnico autorizado evaluará el problema y determinará si está cubierto por la garantía.""",
        help_text="Condiciones y procedimientos para reparaciones cubiertas por garantía"
    )
    
    # Sección de sustitución
    condiciones_sustitucion = models.TextField(
        "Condiciones de Sustitución",
        default="""Situaciones que justifican la sustitución:
- El problema no puede repararse de manera económica o efectiva.
- El dispositivo tiene un defecto de fábrica grave.
- Todo ello será avalado por el fabricante.""",
        help_text="Condiciones bajo las cuales se reemplazará el producto"
    )
    
    # Sección de costos
    politicas_costos = models.TextField(
        "Políticas de Costos",
        default="""- Cubierto por la garantía: Reparación o sustitución gratuita.
- No cubierto por la garantía: Cliente paga costos de reparación/sustitución.
- En caso de defecto de fabricación cubierto, nos comprometemos a reparar o reemplazar su estación de energía.""",
        help_text="Políticas sobre costos de reparación y sustitución"
    )
    
    # Procedimiento para reclamo
    procedimiento_reclamo = models.TextField(
        "Procedimiento para Reclamo",
        default="""1. Contacto: Llamar a Tamara Reinosa Ferrer (asistencia técnica y garantía Fueta International) al celular 59423597 o escribir por WhatsApp al mismo número.
2. Revisión: Presentar la factura de compra y modelo de garantía.
3. Evaluación: El equipo técnico determinará si aplica la garantía.
4. Solución: Se procederá con la reparación, reemplazo o reembolso según corresponda.""",
        help_text="Pasos a seguir para hacer un reclamo de garantía"
    )

    

    def __str__(self):
        return f"Garantia: {self.num}"
    
    class Meta:
        verbose_name = "Registro de Garantia"
        verbose_name_plural = "Registros de Garantia"


@receiver(pre_save, sender=Garantia_P)
def set_numero(sender, instance, **kwargs):
    if not instance.num:
        last_reporte = Garantia_P.objects.order_by('-num').first()
        instance.num = (last_reporte.num + 1) if last_reporte else 1