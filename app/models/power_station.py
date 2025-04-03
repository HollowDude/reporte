from datetime import datetime
from django.db import models

class Power_Station(models.Model):
    TIPO_CHOICES = [
        ('1-300w', '1-300W'),
        ('2-600w', '2-600W'),
        ('3-1200w', '3-1200W'),
        ('4-2400w', '4-2400W'),
        ('5-3000w', '5-3000W'),
    ]
    
    sn = models.CharField("ID", max_length=255, primary_key=True)
    fecha_armado = models.DateField(default=datetime.now)
    tipo = models.CharField("Tipo", max_length=10, choices=TIPO_CHOICES)
    w = models.IntegerField("Watts", editable=False)
    paneles = models.IntegerField("Paneles", editable=False)
    expansiones = models.IntegerField("Expansiones", editable=False)
    bases = models.IntegerField("Bases de Paneles", editable=False)

    def __str__(self):
        return f"ID: {self.sn} Tipo: {self.tipo}"

    def save(self, *args, **kwargs):
        tipo_mapping = {
            '1-300w': {'w': 300, 'paneles': 1, 'expansiones': 4, 'bases': 2},
            '2-600w': {'w': 600, 'paneles': 1, 'expansiones': 4, 'bases': 2},
            '3-1200w': {'w': 1200, 'paneles': 2, 'expansiones': 8, 'bases': 4},
            '4-2400w': {'w': 2400, 'paneles': 3, 'expansiones': 12, 'bases': 6},
            '5-3000w': {'w': 3000, 'paneles': 3, 'expansiones': 12, 'bases': 6},
        }
        if self.tipo in tipo_mapping:
            data = tipo_mapping[self.tipo]
            self.w = data['w']
            self.paneles = data['paneles']
            self.expansiones = data['expansiones']
            self.bases = data['bases']
        super().save(*args, **kwargs)