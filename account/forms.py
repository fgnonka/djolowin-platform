from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from .validation_functions import (
    signup_form_clean_email,
    signup_form_clean_username,
    update_form_clean_email,
    update_form_clean_username,
)

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    email = forms.EmailField()

    class Meta:
        """ This class is used to define the fields that will be used in the form."""
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Enter your username"
        self.fields["email"].widget.attrs["placeholder"] = "Enter your email"
        self.fields["password1"].widget.attrs["placeholder"] = "Enter your password"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm your password"

    def clean_username(self):
        """ " This method is used to validate the username field against the DEFAULT_RESERVED_NAMES"""
        return signup_form_clean_username(self)

    def clean_email(self):
        """This method is used to validate the email field of the signup form."""
        return signup_form_clean_email(self)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "country",
            "profile_img",
        ]

    def clean_username(self):
        return update_form_clean_username(self)

    def clean_email(self):
        return update_form_clean_email(self)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
