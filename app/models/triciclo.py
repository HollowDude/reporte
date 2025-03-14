from datetime import datetime
from django.db import models

class Triciclo(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.vin} - {self.fecha_armado}"