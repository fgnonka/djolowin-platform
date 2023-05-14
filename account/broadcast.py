from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from communication.models import Notification, AbstractEmail
from communication.utils import create_abstract_email, create_user_abstract_email

from .tokens import account_activation_token, decode_token_check, encode_token


def send_activation_email(user):
    current_site = get_current_site(user)
    subject = "Activate your account."
    message = render_to_string(
        "djolowin/account/activation_email.html",
        {
            "from_email": settings.DEFAULT_FROM_EMAIL,
            "protocol": "http",
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    create_abstract_email(email)
    email.send()


def send_welcome_notification(user):
    subject = "Welcome to Djolowin!"
    message = render_to_string(
        "djolowin/communication/notifications/account/welcome_notification.html",
        {"user": user},
    )
    Notification.objects.create(
        recipient=user,
        subject=subject,
        body=message,
    )


def send_welcome_email(user):
    subject = "Welcome to Djolowin!"
    message = render_to_string(
        "djolowin/communication/emails/account/welcome_email.html",
        {"user": user},
    )
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    create_user_abstract_email(email, user)
    email.send()


def send_password_change_alert_email(user):
    subject = "Password change alert"
    message = render_to_string(
        "djolowin/communication/emails/account/password_change_alert_email.html",
        {"user": user},
    )
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    create_user_abstract_email(email, user)
    email.send()


def send_email_change_alert_email(user):
    subject = "Email change alert"
    message = render_to_string(
        "djolowin/communication/emails/account/email_changed_body.html",
        {"user": user},
    )
    to_email = user.email
    email = EmailMessage(subject, message, to=[to_email])
    create_user_abstract_email(email, user)
    email.send()


def send_email_change_request(old_user, new_email):
    # Generate the token
    current_site = get_current_site(old_user)
    uid, token = encode_token(old_user)

    # Send the activation email
    subject = "Confirm your email change"
    message = render_to_string(
        "djolowin/account/email_change_request.html",
        {
            "protocol": "http",
            "user": old_user,
            "domain": current_site,
            "uid": uid,
            "token": token,
            "new_email": new_email,
        },
    )
    email = EmailMessage(subject, message, to=[old_user.email])
    email.send()
