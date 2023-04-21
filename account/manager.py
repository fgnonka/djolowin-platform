from django.contrib.auth.models import BaseUserManager
from django.db.models.expressions import Exists, OuterRef
from django.db.models import Q
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD + '__iexact': username})

    def get_or_create(self, email, **defaults):
        if email is None:
            email = defaults.pop('username', None)
        if email is None:
            raise ValueError('Either email or username must be given')
        try:
            return self.get(email=email), False
        except self.model.DoesNotExist:
            defaults.setdefault('username', get_random_string(32))
            return self.create(email=email, **defaults), True

    def filter_by_email(self, email):
        return self.filter(email__iexact=email)

    def filter_by_email_or_username(self, email):
        return self.filter(
            Q(email__iexact=email) | Q(username__iexact=email)
        )

    def filter_by_email_or_username_or_phone(self, email):
        return self.filter(
            Q(email__iexact=email) | Q(username__iexact=email) | Q(phone__iexact=email)
        )

    def filter_by_email_or_username_or_phone_or_name(self, email):
        return self.filter(
            Q(email__iexact=email) | Q(username__iexact=email) | Q(phone__iexact=email) | Q(name__iexact=email)
        )
    