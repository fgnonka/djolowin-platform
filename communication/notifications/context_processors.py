from communication.models import Notification

def notifications(request):
    context = {}
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user)
        unread_notifications = Notification.objects.filter(recipient=request.user, date_read= None)
        return {"notifications": notifications, "unread_notifications": unread_notifications}
    return context
