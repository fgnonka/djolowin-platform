from django.shortcuts import redirect
from django.conf import settings

class CustomDispatchMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(CustomDispatchMixin, self).dispatch(request, *args, **kwargs)