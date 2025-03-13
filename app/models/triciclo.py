from django.db import models

class Triciclo(models.Model):
    vin = models.CharField("Vin", max_length=255, primary_key=True)

    def __str__(self):
        return f"{self.vin}"