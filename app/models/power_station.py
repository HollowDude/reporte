from django.db import models

class Power_Station(models.Model):
    sn = models.CharField("S/N", max_length=255, primary_key=True)

    def __str__(self):
        return f"{self.sn}"