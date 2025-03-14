from datetime import datetime
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .triciclo import Triciclo
from .power_station import Power_Station
from .cliente import Cliente
from .empresa import Empresa



class Registro(models.Model):

    fecha_armado = models.DateField(default=datetime.now)
    fecha_entregado = models.DateField(blank=True, null=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    llamada = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    triciclo = models.ForeignKey(Triciclo, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.numero_reporte}"

@receiver(pre_save, sender=Registro)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1


class Registro_Pendiente(models.Model):

    fecha_armado = models.DateField()
    fecha_entregado = models.DateField(blank=True, null=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    autorizado = models.BooleanField(default=False)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    triciclo = models.ForeignKey(Triciclo, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.numero_reporte}"

@receiver(pre_save, sender=Registro_Pendiente)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1