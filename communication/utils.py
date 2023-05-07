import logging

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string

from communication.models import Notification, AbstractEmail, CommunicationEventType


class Dispatcher(object):
    def __init__(self, logger=None, mail_connection=None):
        if not logger:
            logger = logging.getLogger(__name__)
        self.logger = logger
        self.mail_connection = mail_connection

    # Public API methods and properties

    def create_abstract_email(self, email):
        """
        Create an abstract email object for a given email.
        """
        return AbstractEmail.objects.create(
            subject=email.subject,
            body_text=email.body,
            from_email=email.from_email,
            to_email=email.to,
        )

    def send_user_email_messages(self, user, messages, attachements=None):
        """Send email messages to a user"""
        if not user.email:
            self.logger.warning(
                "Not sending email to user '%s' as no email address is set.", user
            )
            return None
        email = self.send_email_messages(user.email, messages, attachements)

        if settings.DJOLOWIN_SAVE_SENT_EMAILS_TO_DB:
            self.create_abstract_email(email)

        return email

    def send_email_messages(
        self, recipient_email, messages, from_email=None, attachements=None
    ):
        """
        Send email messages to a recipient email address
        """
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL
        email = EmailMultiAlternatives(
            subject=messages["subject"],
            body=messages["body"],
            from_email=from_email,
            to=[recipient_email],
            attachments=attachements,
        )
        if "html" in messages:
            email.attach_alternative(messages["html"], "text/html")

        self.logger.info("Email sent to %s" % recipient_email)
        email.send()

        return email

    def get_messages(self, event_code, extra_context=None):
        """
        Return rendered messages
        """
        if extra_context is None:
            extra_context = {}
        context = self.get_base_context(**extra_context)

        msgs = CommunicationEventType.objects.get_and_render(event_code, context)
        return msgs


def create_email(subject, template_name, context, to_email):
    message = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    return email
