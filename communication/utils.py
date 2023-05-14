import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string

from communication.models import Notification, AbstractEmail
from account.models import CustomUser as User


def create_email_from_html(subject, template_name, context, to_email):
    message = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    return email


def send_email(subject, template_name, context, to_email):
    email = create_email_from_html(subject, template_name, context, to_email)
    email.send()


def create_abstract_email(email):
    abstract_email = AbstractEmail(
            subject=email.subject, body_text=email.body, email=email.to
    )
    abstract_email.save()

def create_user_abstract_email(email, user):
    abstract_email = AbstractEmail(
            subject=email.subject, body_text=email.body, email=email.to, user=user
    )
    abstract_email.save()