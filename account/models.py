from uuid import uuid4

from django.core.mail import send_mail
from django.db.models import JSONField
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.forms.models import model_to_dict

from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from django_countries.fields import CountryField, Country
from PIL import Image

from wallet.models import UserWallet
from .manager import CustomUserManager
from . import CustomerEvents


class Address(models.Model):
    """ A model to represent a user's address."""
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = models.CharField(max_length=255, blank=True)
    country = CountryField(blank=True)
    postal_code = models.CharField(max_length=255, blank=True)

    @property
    def full_name(self):
        """ Property returning the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.full_name}--{self.address}--{self.city}--{self.country}"

    def __eq__(self, other):
        if not isinstance(other, Address):
            return False
        return self.as_data == other.as_data

    class Meta:
        ordering = ("pk",)
        indexes = [
            models.Index(fields=["first_name", "last_name"]),
            models.Index(fields=["address"]),
            models.Index(fields=["city"]),
            models.Index(fields=["state"]),
            models.Index(fields=["country"]),
            models.Index(fields=["postal_code"]),
        ]

    def as_data(self):
        data = model_to_dict(self, exclude=["id", "user"])
        if isinstance(data["country"], Country):
            data["country"] = data["country"].code
        return data

    def get_copy(self):
        return Address.objects.create(**self.as_data())


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Each `User` needs a human-readable unique identifier that we can use to
    represent the `User` in the UI. We want to index this column in the
    database to improve lookup performance"""
    username = models.CharField(
        _("username"),
        db_index=True,
        max_length=20,
        unique=True,
        blank=False,
        null=False,
    )
    first_name = models.CharField(_("first name"), max_length=100, blank=True)
    last_name = models.CharField(_("Last name"), max_length=50, blank=True, null=True)
    # We also need a way to contact the user and a way for the user to identify
    # themselves when logging in. Since we need an email address for contacting
    # the user anyways, we will also use the email for logging in because it is
    # the most common form of login credential at the time of writing.
    email = models.EmailField(_("Email address"), unique=True)

    country = CountryField(_("Country"), blank=True)
    default_billing_address = models.ForeignKey(
        Address, related_name="+", null=True, blank=True, on_delete=models.SET_NULL
    )
    date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
    profile_img = models.ImageField(
        default="default.png", upload_to="profile_images", blank=True, null=True
    )
    phone_number = PhoneNumberField(blank=True, default="", db_index=True)

    # User Status
    # A timestamp representing when this object was created.
    date_joined = models.DateTimeField(_("Date joined"), auto_now_add=True)
    last_login = models.DateTimeField(_("Last login"), blank=True, null=True)
    # A timestamp representing when this object was created.
    updated_at = models.DateTimeField(auto_now=True)

    # The `is_staff` flag is expected by Django to determine who can and cannot
    # log into the Django admin site. For most users this flag will always be
    # false.
    is_staff = models.BooleanField(_("Admin status"), default=False)

    # The 'is_superuser' flag is expected by Django to determine who can and
    # cannot access the admin site and perform all administrative actions.
    is_superuser = models.BooleanField(_("Superuser status"), default=False)

    # When a user no longer wishes to use our platform, they may try to delete
    # their account. That's a problem for us because the data we collect is
    # valuable to us and we don't want to delete it. We
    # will simply offer users a way to deactivate their account instead of
    # letting them delete it. That way they won't show up on the site anymore,
    # but we can still analyze the data.
    is_active = models.BooleanField(_("Active"), default=True)
    is_verified = models.BooleanField(_("Verified"), default=False)
    note = models.TextField(null=True, blank=True)
    search_document = models.TextField(blank=True, default="")
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    
    

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    # In this case we want it to be the email field.
    USERNAME_FIELD = "email"

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    objects = CustomUserManager()


    class Meta:
        ordering = ("pk",)
        indexes = [
            models.Index(fields=["username"]),
            models.Index(fields=["email"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["country"]),
        ]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._effective_permissions = None

    def __str__(self):
        """ Human-readable representation that overrides the default one that
        returns the username field."""
        return str(self.uuid)
    
    def save(self, *args, **kwargs):
        self.search_document = self.get_search_document()
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)

        img = Image.open(self.profile_img.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_img.path)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        if self.first_name and self.last_name:
            full_name = f"{self.first_name} {self.last_name}"
            return full_name.strip()
        else:
            return self.email

    def get_search_document(self):
        """ Returns a string used for indexing this object in a search engine."""
        document = self.username
        if self.first_name:
            document += f" {self.first_name}"
        if self.last_name:
            document += f" {self.last_name}"
        if self.email:
            document += f" {self.email}"
        if self.phone_number:
            document += f" {self.phone_number}"
        if self.country:
            document += f" {self.country.name}"
        return document

    def email_user(self, subject, message, from_email=None, **kwargs):
        """ Sends an email to this user."""
        send_mail(
            subject, message, from_email, [self.email], fail_silently=False, **kwargs
        )

    def get_absolute_url(self):
        """ Return the URL to the user detail page."""
        return reverse("account:user-detail", kwargs={"username": self.username})


class CustomerEvent(models.Model):
    """ Records events that happened during the customer lifecycle."""
    date = models.DateTimeField(_("Date"), auto_now_add=True)
    event_type = models.CharField(
        _("Event type"),
        max_length=255,
        choices=[
            (type_name.upper(), type_name) for type_name, _ in CustomerEvents.CHOICES
        ],
    )
    user = models.ForeignKey(CustomUser, related_name="events", on_delete=models.CASCADE, null=True)
    parameters = JSONField(_("Event parameters"), blank=True, default=dict)
    
    class Meta:
        ordering = ("date",)
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(type={self.event_type!r}, user={self.user!r})"
