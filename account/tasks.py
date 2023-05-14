from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .broadcast import send_activation_email, send_welcome_notification, send_welcome_email
from .signals import user_verified

User = get_user_model()

@receiver(post_save, sender=User)
def generate_activation_email(sender, instance, created, **kwargs):
    if created:
        send_activation_email(instance)
        

@receiver(user_verified)
def generate_welcome_notification_and_email(sender, instance, **kwargs):
    send_welcome_notification(instance)
    send_welcome_email(instance)