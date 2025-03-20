from celery import shared_task
from datetime import date
from app.models.registro import Registro

@shared_task
def actualizar_tiempoR():
    registros = Registro.objects.all()
    for registro in registros:
        dias_transcurridos = (date.today() - registro.fecha_entregado).days
        registro.tiempoR = max(0, 180 - dias_transcurridos)
        registro.save()