from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.email}"