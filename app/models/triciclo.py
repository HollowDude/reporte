from datetime import date, datetime
from django.db import models
from django.dispatch import receiver
from django.forms import ValidationError
from django.db.models.signals import pre_save

class Triciclo(models.Model):
    MODELOS = [
        ('triciclo con extensor de rango', 'TRICICLO CON EXTENSOR DE RANGO'),
        ('triciclo eléctrico de carga', 'TRICICLO ELÉCTRICO DE CARGA'),
        ('triciclo eléctrico con panel solar', 'TRICICLO ELÉCTRICO CON PANEL SOLAR'),
        ('moto ry', 'MOTO RY'),
        ('cuatriciclo t90', 'CUATRICICLO T90'),
    ]




    vin = models.CharField("Vin", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now, help_text="Fecha en que se armo el triciclo")
    num_m = models.CharField("Numero de Motor", max_length = 255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    fecha_autorizado = models.DateField(blank = True, null = True, help_text="Aparecera automaticamente al autorizar el triciclo")
    autorizado = models.BooleanField(default=False, help_text="El triciclo se autorizara solo por el encargado de ello")
    obser = models.TextField("Observaciones adicionales", help_text="Algunas observaciones sobre el triciclo que pueden ser modificadas a lo largo del tiempo")
    modelo = models.CharField("Modelo", max_length=255, choices=MODELOS ,help_text="Modelo del Triciclo")
    vendido = models.BooleanField("Vendido", default=False, help_text="Cuando se realice una relacion de venta de triciclo se vera reflejado aqui")
    fecha_v = models.DateField("Fecha de Venta", default=None, null=True, blank=True, help_text="Al marcarse como vendido un triciclo la fecha se actualiza")

    def __str__(self):
        return f"VIN: {self.vin} - Modelo: {self.modelo}"

    def clean(self):
        super().clean() 
        if len(self.vin) != 17:  
            raise ValidationError({"vin": "El VIN debe tener exactamente 17 dígitos."})

    class Meta:
        verbose_name = "Triciclo Armado"
        verbose_name_plural = "Triciclos Armados"

@receiver(pre_save, sender=Triciclo)
def set_fecha_auth(sender, instance, **kwargs):
    if instance.autorizado and not instance.fecha_autorizado:
        instance.fecha_autorizado = date.today()

        