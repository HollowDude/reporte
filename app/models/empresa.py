from django.db import models

class Empresa(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    nit = models.CharField("NIT",max_length = 255, blank = True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Registro de MIPYME: {self.nombre}"
    
    class Meta:
        verbose_name = "Registro de MIPYME"
        verbose_name_plural = "Registros de MIPYME"