from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic
from communication.notifications.views import DetailView, ArchiveView, InboxView

from .views import MessageAPIView

notification_inbox_view = InboxView.as_view()
notification_archive_view = ArchiveView.as_view()
notification_detail_view = DetailView.as_view()

app_name = 'communication'

urlpatterns = [
    # Notifications
            # Redirect to notification inbox
            path(
                'notifications/', generic.RedirectView.as_view(url='communication:notifications-inbox', permanent=False)),
            path(
                'notifications/inbox/',
                login_required(notification_inbox_view),
                name='notifications-inbox'),
            path(
                'notifications/archive/',
                login_required(notification_archive_view),
                name='notifications-archive'),
            path(
                'notifications/<int:pk>/',
                login_required(notification_detail_view),
                name='notification-detail'),
            
    #TESts urls for notifications using pusher
            path('messages/', MessageAPIView.as_view(), name='messages'),
]
