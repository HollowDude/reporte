from datetime import date
from django.db import models
from django.dispatch import receiver
from .cliente import Cliente
from.empresa import Empresa
from .power_station import Power_Station
from django.db.models.signals import pre_save

class Garantia_P(models.Model):
    num = models.IntegerField("Numero de Garantia", primary_key=True, help_text="Se genera automaticamente y es secuencial")
    fecha_em = models.DateField("Fecha de Emision", default=date.today())
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL, help_text="Aca estaran los datos especificos de la Power Station y sus paneles asociados, acceder para ver detalles.")


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