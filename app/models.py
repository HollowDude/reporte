from datetime import datetime
from email.policy import default
from random import choice
import uuid
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.forms import ValidationError
from psycopg2 import Date

VALUES = [
        ('power station', 'Power Station'),
        ('triciclo', 'Triciclo')
    ]

# Create your models here.
class Registro_Clientes(models.Model):

    vin = models.CharField(max_length=255, primary_key=True)  
    nombre = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    carnet = models.CharField("Carnet/NIT", max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_armado = models.DateField(default=datetime.now)
    fecha_entregado = models.DateField(blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    llamada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Registro_Clientes)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro_Clientes.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1


class Registro_Clientes_Pendientes(models.Model):

    vin = models.CharField(max_length=255, primary_key=True)  
    nombre = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    carnet = models.CharField("Carnet/NIT", max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_armado = models.DateField()
    fecha_entregado = models.DateField(blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Registro_Clientes_Pendientes)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro_Clientes.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1

class Registro_Empresa(models.Model):

    vin = models.CharField("VIN-S/N", max_length=255, primary_key=True)
    nombre_empresa = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_armado = models.DateField(default=datetime.now)
    fecha_entregado = models.DateField(blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    articulo = models.CharField(max_length = 20, choices=VALUES, default='Triciclo')
    numero_reporte = models.IntegerField(editable=False, unique=True)
    llamada = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Registro_Empresa)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro_Empresa.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1

class Registro_Empresa_Pendientes(models.Model):

    vin = models.CharField("VIN-S/N", max_length=255, primary_key=True)
    nombre_empresa = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    fecha_armado = models.DateField()
    fecha_entregado = models.DateField(blank=True)
    extensor_rango = models.CharField(max_length=255, blank=True)
    sello = models.CharField(max_length=255, default="NONE", blank=True)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    articulo = models.CharField(max_length = 20, choices=VALUES, default='Triciclo')
    autorizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.numero_reporte} - {self.vin}"

@receiver(pre_save, sender=Registro_Empresa_Pendientes)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro_Empresa.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1




class Garantia(models.Model):
    usuario = models.ForeignKey(Registro_Clientes, on_delete=models.CASCADE)
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