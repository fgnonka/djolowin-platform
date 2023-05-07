from django.contrib import admin
from .models import CommunicationEventType, Notification, AbstractEmail
# Register your models here.

admin.site.register(CommunicationEventType)
admin.site.register(Notification)
admin.site.register(AbstractEmail)