from typing import Optional
from urllib.parse import urlencode
from django.contrib.auth.tokens import default_token_generator

from core.notification import get_site_context
from core.utils.url import prepare_url
from .models import CustomUser
from . import CustomerEvents


def get_default_user_payload(user: CustomUser) -> dict:
    """Returns a dictionary of the default user payload."""
    payload = {
        "uuid": str(user.uuid),
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "metadata": user.metadata,
    }
    return payload


def get_user_custom_payload(user: CustomUser) -> dict:
    """Returns a dictionary of the custom user payload."""
    payload = {
        "user": get_default_user_payload(user),
        "recipient_email": user.email,
        **get_site_context(),
    }
    return payload


def send_user_password_reset_notification(
    redirect_url, user, manager, channel_slug: Optional[str], staff=False
):
    """Trigger the user password reset notification event."""
    token = default_token_generator.make_token(user)
    params = urlencode({"email": user.email, "token": token})
    reset_url = prepare_url(params, redirect_url)

    payload = {
        "user": get_default_user_payload(user),
        "recipient_email": user.email,
        "token": token,
        "reset_url": reset_url,
        **get_site_context(),
    }

    event = CustomerEvents.PASSWORD_RESET_LINK_SENT
    manager.notify(event, payload, channel_slug, staff=staff)
