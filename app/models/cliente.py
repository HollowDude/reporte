from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100, blank=True)
    apellidos = models.CharField(max_length=100, blank=True)
    carnet = models.CharField("Carnet", max_length=50, blank=True)
    direccion = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
    class Meta:
        verbose_name = "Registro de T.C.P/P.N"
        verbose_name_plural = "Registros de T.C.P/P.N"