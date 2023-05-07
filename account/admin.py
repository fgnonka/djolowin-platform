""" This module is used to register the models 
of the account app in the admin interface."""""
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from account.forms import UserRegistrationForm
from account.models import CustomerEvent

User = get_user_model()


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        """ Meta class for UserChangeForm"""
        model = User
        fields = (
            "username",
            "email",
            "password",
            "date_of_birth",
            "is_active",
            "is_staff",
        )


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """ The UserAdmin class is used to customize
    the admin interface for the User model."""
    # The forms to add and change user innces
    form = UserChangeForm
    add_form = UserRegistrationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        "uuid",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("is_staff", "date_joined")
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "email",
                    "profile_img",
                    "phone_number",
                )
            },
        ),
        (
            _("Permissions"),
            {"fields": ("is_staff", "is_superuser", "is_active", "groups")},
        ),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "date_of_birth",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email", "date_joined", "username")
    filter_horizontal = ()


@admin.register(CustomerEvent)
class CustomerEventAdmin(admin.ModelAdmin):
    """ The CustomerEventAdmin class is used to customize
    the admin interface for the CustomerEvent model."""
    list_display = ("user", "event_type", "date")
    list_filter = ("event_type", "date")
    ordering = ("date",)
    search_fields = ("user",)
