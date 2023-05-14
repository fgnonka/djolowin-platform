from django.shortcuts import redirect
from django.conf import settings

class CustomDispatchMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(CustomDispatchMixin, self).dispatch(request, *args, **kwargs)


class PageTitleMixin(object):
    """
    Passes page_title and active_tab into context, which makes it quite useful
    for the accounts views.

    Dynamic page titles are possible by overriding get_page_title.
    """
    page_title = None
    active_tab = None

    def get_page_title(self):
        return self.page_title

    def get_context_data(self, **kwargs):
        context = super(PageTitleMixin, self).get_context_data(**kwargs)
        context["page_title"] = self.get_page_title()
        context["active_tab"] = self.active_tab
        return context
    