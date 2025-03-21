from datetime import date
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .triciclo import Triciclo
from .power_station import Power_Station
from .cliente import Cliente
from .empresa import Empresa



class Registro(models.Model):

    fecha_entregado = models.DateField("Puesta en marcha",default = date.today())
    tiempoR = models.IntegerField("Tiempo Restante", editable=False)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    llamada = models.BooleanField("Reporte de reclamacion", default=False)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    triciclo = models.ForeignKey(Triciclo, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Relacion de venta: {self.numero_reporte} - {self.cliente} - {self.empresa} -> {self.triciclo} - {self.power_station}"

    def save(self, *args, **kwargs):

        if not self.pk:
            dias_transcurridos = (date.today() - self.fecha_entregado).days
            self.tiempoR = max(0, 365 - dias_transcurridos) 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Relacion de venta"
        verbose_name_plural = "Relacion de ventas"

@receiver(pre_save, sender=Registro)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1
