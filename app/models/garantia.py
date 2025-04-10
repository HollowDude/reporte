from django.db import models
from .cliente import Cliente
from.empresa import Empresa
from .triciclo import Triciclo
from .power_station import Power_Station
ESPEC = [
    ("abraham pino valdes", "Abraham Pino Valdes"),
    ("juan", "Juan"),
    ("jose", "Jose"),
    ("ailet", "Ailet"),
    ("tamara", "Tamara"),
    ("dago", "Dago"),
    ("roberto", "Roberto"),
]

FACT = [
    ("cliente", "Cliente"),
    ("vendedor", "Vendedor"),
]
class Garantia(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL)
    triciclo = models.ForeignKey(Triciclo, null=True, blank=True, on_delete=models.SET_NULL)
    power_station = models.ForeignKey(Power_Station, null=True, blank=True, on_delete=models.SET_NULL)
    motivo=models.TextField("Motivo", max_length=255)
    evaluacion=models.TextField("Evaluacion resumen", max_length=255)
    trabajos_hechos=models.TextField("Trabajos realizados", max_length=255)
    piezas_usadas=models.TextField("Lista de piezas usadas", max_length=255)
    recomendaciones=models.TextField("Algunas recomendaciones", max_length=255)
    nombre_especialista=models.CharField("Especialista encargado", choices=ESPEC, max_length=255)
    conformidad_cliente=models.BooleanField("Conformidad del cliente")

    def __str__(self):
        if self.cliente:
            if self.triciclo:
                return f"Reporte de Reclamacion: {self.cliente}  -> {self.triciclo}"
            else:
                return f"Reporte de Reclamacion: {self.cliente}  -> {self.power_station}"
        else:
            if self.triciclo:
                return f"Reporte de Reclamacion: {self.empresa}  -> {self.triciclo}"
            else:
                return f"Reporte de Reclamacion: {self.empresa}  -> {self.power_station}"

    class Meta:
        verbose_name = "Reporte de Reclamacion"
        verbose_name_plural = "Reporte de Reclamaciones"

