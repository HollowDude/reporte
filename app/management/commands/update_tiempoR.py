from django.core.management.base import BaseCommand
from datetime import date
from app.models.registro import Registro 

class Command(BaseCommand):
    help = 'Actualiza el campo tiempoR de todos los registros'

    def handle(self, *args, **kwargs):
        registros = Registro.objects.all()
        for registro in registros:
            dias_transcurridos = (date.today() - registro.fecha_entregado).days
            registro.tiempoR = max(0, 180 - dias_transcurridos)
            registro.save()
        self.stdout.write(self.style.SUCCESS('Campo tiempoR actualizado correctamente'))