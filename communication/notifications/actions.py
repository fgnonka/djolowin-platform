from django.utils import timezone
from django.template.loader import render_to_string
from communication.models import Notification

def send_notification(recipient, subject, message):
    # Create a new notification object
    notification = Notification(
        recipient=recipient,
        subject=subject,
        body=message,
        date_sent=timezone.now(),
    )
    notification.save()