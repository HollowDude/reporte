from datetime import date
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save
from .triciclo import Triciclo
from .power_station import Power_Station
from .cliente import Cliente
from .empresa import Empresa


class Registro(models.Model):
    RECEPTOR_CHOICES = [
            ('pino.isaac27@gmail.com', 'Isaac'),
            ('tallerjireh47@gmail.com', 'Mary'),
        ]

    fecha_entregado = models.DateField("Fecha entregado",default = date.today())
    tiempoR = models.IntegerField("Tiempo Restante", editable=False)
    numero_reporte = models.IntegerField(editable=False, unique=True)
    llamada = models.TextField("Reportar por correo(Especificar motivo)", blank = True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL, help_text = "Cliente a ser Reportado")
    empresa = models.ForeignKey(Empresa, null=True, blank=True, on_delete=models.SET_NULL, help_text = "Empresa a ser Reportada")
    triciclo = models.ForeignKey(Triciclo, null=True, blank=True, on_delete=models.SET_NULL)
    receptor = models.CharField(
        "Receptor(es) del correo",
        max_length=255,
        blank=True,
        help_text="Selecciona uno o varios receptores, o Todos"
    )

    def __str__(self):
        if self.cliente:
            return f"Relacion de venta: {self.numero_reporte} - {self.cliente}  -> {self.triciclo}"
        else:
            return f"Relacion de venta: {self.numero_reporte} - {self.empresa}  -> {self.triciclo}"

    def save(self, *args, **kwargs):

        if not self.pk:
            dias_transcurridos = (date.today() - self.fecha_entregado).days
            self.tiempoR = max(0, 365 - dias_transcurridos) 
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Relacion de venta"
        verbose_name_plural = "Relacion de ventas"

@receiver(pre_save, sender=Registro)
def set_numero_reporte(sender, instance, **kwargs):
    if not instance.numero_reporte:
        last_reporte = Registro.objects.order_by('-numero_reporte').first()
        instance.numero_reporte = (last_reporte.numero_reporte + 1) if last_reporte else 1
    if instance.triciclo:
        instance.triciclo.vendido = True
        instance.triciclo.fecha_v = date.today()
        instance.triciclo.save()
        
