# In a new file called decorators.py or in your existing views.py file
from functools import wraps
from django.http import HttpResponseForbidden

def user_is_active(function):
    @wraps(function)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_active:
            return function(request, *args, **kwargs)
        else:
            return  HttpResponseForbidden("You need to verify your email address to access this page.")
    return _wrapped_view
