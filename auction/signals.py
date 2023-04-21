# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Bid
from .tasks import send_outbid_notification, send_auction_ending_soon_notifications


@receiver(post_save, sender=Bid)
def notify_outbid_user(sender, instance, created, **kwargs):
    if created:
            # Call the Celery task to send a notification to the outbid user
            send_outbid_notification.delay(instance.id)


@receiver(post_save, sender=Bid)
def auction_ending_soon(sender, instance, created, **kwargs):
    if created:
        send_auction_ending_soon_notifications.delay()
