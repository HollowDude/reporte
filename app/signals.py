from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import registro

@receiver(post_save, sender=registro.Registro)
def enviar_notificacion_email(sender, instance, **kwargs):
    if instance.llamada and instance.receptor:
        # Obtener datos del comprador
        comprador = instance.cliente if instance.cliente else instance.empresa
        comprador_data = "\n".join([f"{key}: {value}" for key, value in comprador.__dict__.items() if not key.startswith('_')])
        
        # Obtener datos del producto
        if instance.triciclo:
            producto = instance.triciclo 
        if  instance.power_station:
            producto = instance.power_station
        else:
            producto = instance.panel 
        producto_data = "\n".join([f"{key}: {value}" for key, value in producto.__dict__.items() if not key.startswith('_')])
        
        # Construir mensaje
        subject = f"Reporte de Cliente: {comprador.nombre}"
        message = (
            f"Datos del Comprador:\n{comprador_data}\n\n"
            f"Datos del Producto:\n{producto_data}\n\n"
            f"Motivo del Reporte: {instance.llamada}"
        )
        
        # Procesar receptores
        recipients = instance.receptor.split(',')
        if 'tallerjireh47@gmail.com' in recipients:
            recipients = [email for email, _ in registro.Registro.RECEPTOR_CHOICES if email != 'tallerjireh47@gmail.com']
        send_mail(
            subject,
            message,
            None,
            recipients,
            fail_silently=False,
        )