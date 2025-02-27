from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Reporte(models.Model):

    vin = models.CharField(max_length=255, primary_key=True)  
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    carnet = models.CharField(max_length=50)
    direccion = models.TextField()
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    fecha_armado = models.DateField()
    fecha_entregado = models.DateField()
    extensor_rango = models.CharField(max_length=255, unique=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Reporte)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Reporte.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1