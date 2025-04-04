from datetime import datetime
import uuid
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
    aut = models.BooleanField("Kit Autorizado", default = False, help_text="El kit se autorizara solo por el encargado de ello")
    cuchilla = models.CharField("Cuchilla", choices = TIPO_C, max_length = 255)
    act = models.CharField("Actualizacion de Software", choices = DES, max_length = 255)
    num = models.CharField("Numero de Serie", max_length=255, default=uuid.uuid4)
    
    def __str__(self):
        return f"ID: {self.id}, Kit: {self.kit}"
    
    class Meta:
        verbose_name = "Panel Solar"
        verbose_name_plural = "Paneles Solares"
