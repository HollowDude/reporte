from datetime import datetime
from django.db import models

class Triciclo(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)
    num_m = models.CharField("Numero de Motor", max_length = 255, blank=True)
    modelo = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.vin} - {self.modelo}"


class Triciclo_Pendiente(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)
    num_m = models.CharField("Numero de Motor", max_length = 255, blank=True)
    modelo = models.CharField(max_length=255, blank=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vin} - {self.modelo}"