import datetime
from django.contrib import messages
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect
from django.views.generic import View

from .models import CheckInHistory


class CheckInMixin:
    @classmethod
    def get_check_in_window(cls, request):
        now = datetime.datetime.now()

        # Get the current check-in window.
        check_in_window = ""
        if now.time() >= datetime.time(6, 0) and now.time() <= datetime.time(14, 0):
            check_in_window = f"{now.date()}---6am-2pm"
        elif now.time() >= datetime.time(14, 0) and now.time() <= datetime.time(22, 0):
            check_in_window = f"{now.date()}---2pm-10pm"
        elif (
            now.time() >= datetime.time(22, 0) and now.time() <= datetime.time(23, 59)
        ) or (now.time() >= datetime.time(0, 0) and now.time() <= datetime.time(6, 0)):
            check_in_window = f"{now.date()}---10pm-6am"
            
        # Check if the user has already checked in for the current check-in window.
        if CheckInHistory.objects.filter(user=request.user, check_in_window=check_in_window).exists():
            messages.error(request, "You have already checked in for the current check-in window.")
            return redirect("account:user-redirect")

        # Create a new check-in history entry for the user with the current time.
        CheckInHistory.objects.create(user=request.user, check_in_time=now, check_in_window=check_in_window)
        messages.success(request, "You have successfully checked in.")
        return redirect("base:home")


# Create a Django decorator to decorate the check-in view.
def check_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("account:login")
        return view_func(request, *args, **kwargs)

    return wrapper
