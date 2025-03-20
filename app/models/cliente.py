from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    carnet = models.CharField("Carnet/NIT", max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Registro de cliente: {self.nombre} {self.apellidos}"
    
    class Meta:
        verbose_name = "Registro de cliente"
        verbose_name_plural = "Registros de cliente"