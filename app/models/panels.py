from datetime import datetime
from django.db import models

class Panels(models.Model):
    TIPO_C = [
        ('manual', 'Manual'),
        ('automatica', 'Automatica'),
    ]
    DES = [
        ('si', 'Si'),
        ('no', 'No')
    ]

    id = models.CharField("ID", primary_key = True)
    kit = models.CharField("Kit de Montaje", max_length = 255)
    cuchilla = models.CharField("Cuchilla", choices = TIPO_C, max_length = 255)
    act = models.CharField("Actualizacion de Software", choices = TIPO_C, max_length = 255)
    
    def __str__(self):
        return f"Panel Solar {self.id}"
    
    class Meta:
        verbose_name = "Panel Solar"
        verbose_name_plural = "Paneles Solares"
