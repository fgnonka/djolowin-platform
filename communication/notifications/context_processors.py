from communication.models import Notification

def notifications(request):
    context = {}
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(recipient=request.user)
        return {"notifications": notifications}
    return context