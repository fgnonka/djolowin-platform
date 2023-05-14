from django.dispatch import Signal

user_signed_up = Signal()
user_verified = Signal()

user_password_reset_link_sent = Signal()
user_password_reset = Signal()
user_password_changed = Signal()

user_email_change_request = Signal()
user_email_changed = Signal()

user_phone_change_request = Signal()
user_phone_changed = Signal()
