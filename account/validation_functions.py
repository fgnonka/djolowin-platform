""" This module contains the clean functions used in the forms of the account app.""" ""
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .validators import (
    DEFAULT_RESERVED_NAMES,
    validate_confusables,
    validate_confusables_email,
)

User = get_user_model()


def check_username_length(username):
    """This method is used to check the length of the username."""
    if len(username) < 3:
        raise forms.ValidationError(_("Username must be at least 3 characters long."))
    return username


def check_username_in_reserved_names(username):
    """This method is used to check if the username is in the DEFAULT_RESERVED_NAMES."""
    if username in DEFAULT_RESERVED_NAMES:
        raise forms.ValidationError(_("This username is reserved and cannot be used."))
    return username


def check_username_exists(username):
    """This method is used to check if the username exists."""
    if not User.objects.filter(username__iexact=username).exists():
        raise forms.ValidationError(_("A user with that username does not exist."))
    return username


def signup_form_clean_username(self):
    """This method is used to validate the username field against the DEFAULT_RESERVED_NAMES"""
    username = self.cleaned_data.get("username")
    check_username_length(username)
    check_username_in_reserved_names(username)
    check_username_exists(username)
    validate_confusables(username)
    return username


def signup_form_clean_email(self):
    """This method is used to validate the email field of a signup form."""
    email = self.cleaned_data.get("email")
    if User.objects.filter(email__iexact=email).exists():
        raise forms.ValidationError(_("A user with that email already exists."))
    validate_confusables_email(email)
    return email


def update_form_clean_username(self):
    """This method is used to validate the username field of a form."""
    username = self.cleaned_data.get("username")
    check_username_length(username)
    check_username_in_reserved_names(username)
    queryset = User.objects.filter(username__iexact=username).exclude(
        pk=self.instance.pk
    )
    if queryset.exists():
        raise forms.ValidationError(_("Username already exists"))
    validate_confusables(username)
    return username


def update_form_clean_email(self):
    """This method is used to validate the email field of a form."""
    email = self.cleaned_data.get("email")
    queryset = User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk)
    if queryset.exists():
        raise forms.ValidationError(_("Email already exists"))
    validate_confusables_email(email)
    return email
