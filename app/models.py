from email.policy import default
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Reporte(models.Model):

    vin = models.CharField(max_length=255, primary_key=True)  
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    carnet = models.CharField("Carnet/NIT", max_length=50)
    direccion = models.TextField()
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20)
    fecha_armado = models.DateField()
    fecha_entregado = models.DateField()
    extensor_rango = models.CharField(max_length=255, unique=True)
    sello = models.CharField(max_length=255, default="NONE")
    numero_reporte = models.IntegerField(editable=False, unique=True)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Reporte)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Reporte.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1

class Garantia(models.Model):
    usuario = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    vin=models.CharField(max_length=255, primary_key=True)
    modelo = models.CharField(max_length=50)
    motor_num=models.CharField(max_length=255)
    fecha_fabr= models.DateField()
    peso=models.FloatField()
    voltaje=models.IntegerField()
    potencia=models.FloatField()
    motivo=models.TextField()
    evaluacion=models.TextField()
    trabajos_hechos=models.TextField()
    piezas_usadas=models.TextField()
    recomendaciones=models.TextField()
    nombre_especialista=models.CharField(max_length=50)
    conformidad_cliente=models.BooleanField()
    facturar_a=models.CharField(default="Cliente")