from django.apps import AppConfig
from .signals import user_signed_up, user_verified

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    def ready(self):
        import account.tasks
        user_signed_up.connect(account.tasks.generate_activation_email)
        user_verified.connect(account.tasks.generate_welcome_notification_and_email)