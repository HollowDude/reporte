from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import registro

@receiver(post_save, sender=registro.Registro)
def enviar_notificacion_email(sender, instance, **kwargs):
    # Si 'llamada' es True y antes no lo era, enviar correo
    if instance.llamada:
        subject = "Notificación de Cliente Contactado"
        message = f"El cliente {instance.cliente} ha sido contactado."
        recipient_list = ["tallerjireh47@gmail.com"]  # Cambia esto al correo de destino

        send_mail(subject, message, None, recipient_list)
        print(f"Correo enviado a {recipient_list}")
