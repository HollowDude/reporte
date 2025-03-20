from datetime import datetime
from django.db import models
from django.forms import ValidationError

class Triciclo(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)
    num_m = models.CharField("Numero de Motor", max_length = 255, blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Triciclo armado: {self.vin} - {self.extensor_rango}"

    def clean(self):
        super().clean() 
        if len(self.vin) != 17:  
            raise ValidationError({"vin": "El VIN debe tener exactamente 17 dígitos."})

    class Meta:
        verbose_name = "Triciclo Armado"
        verbose_name_plural = "Triciclos Armados"


class Triciclo_Pendiente(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)
    num_m = models.CharField("Numero de Motor", max_length = 255, blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"Triciclo con puesta en marcha:{self.vin} - {self.extensor_rango}"
    
    def clean(self):
        super().clean()  
        if len(self.vin) != 17:  
            raise ValidationError({"vin": "El VIN debe tener exactamente 17 dígitos."})
        
    class Meta:
        verbose_name = "Triciclo con puesta en marcha"
        verbose_name_plural = "Triciclos con puesta en marcha"