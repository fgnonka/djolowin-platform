from django.conf import settings
from django.utils.html import strip_tags
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.views import generic

from account.mixins import PageTitleMixin
from communication.models import Notification


class NotificationListView(PageTitleMixin, generic.ListView):
    """A list of all notifications for the current user."""

    model = Notification
    template_name = "djolowin/communication/notifications/notification_list.html"
    context_object_name = "notifications"
    paginate_by = settings.DJOLOWIN_NOTIFICATIONS_PER_PAGE
    page_title = _("Notifications")
    active_tab = "notifications"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_type"] = self.list_type


class InboxView(NotificationListView):
    """A list of unread notifications for the current user."""

    list_type = "inbox"

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user, location="Inbox"
        )


class ArchiveView(NotificationListView):
    """A list of read notifications for the current user."""

    list_type = "archive"

    def get_queryset(self):
        return Notification.objects.filter(
            recipient=self.request.user, location="Archive"
        )


class DetailView(PageTitleMixin, generic.DetailView):
    model = Notification
    template_name = "djolowin/communication/notification_detail.html"
    context_object_name = "notification"
    active_tab = "notifications"
    
    def get_object(self, queryset=None):
        notification = super().get_object(queryset)
        if not notification.date_read:
            notification.date_read = now()
            notification.save()
        return notification
    
    def get_page_title(self):
        title = strip_tags(self.object.subject)
        return f'{title} - {_("Notification")}'
    
    def get_queryset(self):
        return self.model.objects.filter(recipient=self.request.user)
    
