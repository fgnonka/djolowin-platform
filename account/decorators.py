""" Decorators for the account app. """
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def user_is_active(function):
    """Decorator to check if the user is active."""

    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            messages.error(
                request, "You need to verify your email \
                    address to access this page."
            )
            return redirect("account:login")

    return _wrapped_view
