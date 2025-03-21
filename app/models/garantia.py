from django.db import models
from .cliente import Cliente

class Reporte_de_reclamacion(models.Model):
    usuario = models.ForeignKey(Cliente, on_delete=models.CASCADE)
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
