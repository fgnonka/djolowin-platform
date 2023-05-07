from autoslug import AutoSlugField

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.template import engines
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template


from .managers import CommunicationTypeManager

# Create your models here.
User = settings.AUTH_USER_MODEL


class AbstractEmail(models.Model):
    """This is a record of an email sent to a user."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="emails",
        verbose_name=_("User"),
        null=True,
    )
    email = models.EmailField(_("Email Address"), null=True, blank=True)
    subject = models.CharField(_("Subject"), max_length=255)
    body_text = models.TextField(_("Body Text"))
    date_sent = models.DateTimeField(_("Date Sent"), auto_now_add=True)

    class Meta:
        app_label = "communication"
        ordering = ["-date_sent"]
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")

    def __str__(self):
        if self.user:
            return _("Email to %(user)s with subject '%(subject)s'") % {
                "user": self.user.get_username(),
                "subject": self.subject,
            }
        else:
            return _("Email to %(email)s with subject '%(subject)s'") % {
                "email": self.email,
                "subject": self.subject,
            }


class CommunicationEventType(models.Model):
    """A type of communication event. Like an order confirmation email."""

    CATEGORY_CHOICES = (
        ("Card related", _("Card related")),
        ("User related", _("User related")),
        ("Auction related", _("Auction related")),
        ("Payment related", _("Payment related")),
        ("Reward related", _("Reward related")),
    )
    code = AutoSlugField(
        _("Code"),
        max_length=128,
        unique=True,
        populate_from="name",
        editable=True,
        validators=[
            RegexValidator(
                regex=r"^[A-Z_][0-9A-Z_]*$",
                message=_("Code can only contain the characters A-Z, 0-9 and _"),
            ),
        ],
                help_text=_("Code used for looking up this event programatically"),
    )
    name = models.CharField(_("Name"), max_length=255, db_index=True)
    category = models.CharField(_("Category"), max_length=255, choices=CATEGORY_CHOICES)
    # Template content for emails
    # NOTE: There's an intentional distinction between None and ''. None
    # instructs Oscar to look for a file-based template, '' is just an empty
    # template.
    email_subject_template = models.CharField(
        _("Email Subject Template"), max_length=255, blank=True, null=True
    )
    email_body_template = models.TextField(
        _("Email Body Template"), blank=True, null=True
    )
    email_body_html_template = models.TextField(
        _("Email Body HTML Template"),
        blank=True,
        null=True,
        help_text=_("HTML template"),
    )

    # Template content for SMS messages
    sms_template = models.CharField(
        _("SMS Template"),
        max_length=170,
        blank=True,
        null=True,
        help_text=_("SMS template"),
    )

    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    objects = CommunicationTypeManager()

    # File Templates
    email_subject_template_file = (
        "djolowin/communication/emails/commtype_%s_subject.txt"
    )
    email_body_template_file = "djolowin/communication/emails/commtype_%s_body.txt"
    email_body_html_template_file = (
        "djolowin/communication/emails/commtype_%s_body.html"
    )
    sms_template_file = "djolowin/communication/sms/commtype_%s_body.txt"

    class Meta:
        app_label = "communication"
        ordering = ["name"]
        verbose_name = _("Communication Event Type")
        verbose_name_plural = _("Communication Event Types")

    def __str__(self):
        return self.name

    def is_user_related(self):
        return self.category == "User related"

    def is_card_related(self):
        return self.category == "Card related"

    def is_auction_related(self):
        return self.category == "Auction related"

    def is_payment_related(self):
        return self.category == "Payment related"

    def is_reward_related(self):
        return self.category == "Reward related"


class Notification(models.Model):
    LOCATION_CHOICES = (("Inbox", _("Inbox")), ("Archive", _("Archive")))
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    # Not all notifications will have a sender
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(_("Subject"), max_length=255)
    body = models.TextField(_("Body"))
    location = models.CharField(
        max_length=64, choices=LOCATION_CHOICES, default="Inbox"
    )
    date_sent = models.DateTimeField(_("Date Sent"), auto_now_add=True)
    date_read = models.DateTimeField(_("Date Read"), blank=True, null=True)

    class Meta:
        app_label = "communication"
        ordering = ["-date_sent"]
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")

    def __str__(self):
        return self.subject

    def archive(self):
        self.location = "Archive"
        self.save()

    @property
    def is_read(self):
        return self.date_read is not None
