# from django.contrib.auth.tokens import default_token_generator
# from django.urls import reverse
# from django.utils.encoding import force_bytes
# from django.utils.http import urlsafe_base64_encode

# from . import CustomerEvents
# from communication.utils import Dispatcher


# class CustomerDispatcher:
#     """
#     Dispatcher to send concrete customer related emails.
#     """

#     def __init__(self, logger=None, mail_connection=None):
#         self.dispatcher = Dispatcher(logger=logger, mail_connection=mail_connection)

#     def account_created_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.ACCOUNT_CREATED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def account_activated_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.ACCOUNT_ACTIVATED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def account_deactivated_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.ACCOUNT_DEACTIVATED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def send_password_reset_link_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.PASSWORD_RESET_LINK_SENT, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def send_password_changed_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.PASSWORD_CHANGED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def send_email_changed_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.EMAIL_CHANGED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def phonenumber_change_request_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.PHONE_CHANGE_REQUEST, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)

#     def phonenumber_changed_email_for_user(self, user, extra_context):
#         messages = self.dispatcher.get_messages(
#             CustomerEvents.PHONE_CHANGED, extra_context
#         )
#         self.dispatcher.dispatch_user_messages(user, messages)


# def get_password_reset_url(user, token_generator=default_token_generator):
#     """
#     Generate a password-reset URL for a given user
#     """
#     kwargs = {
#         "token": token_generator.make_token(user),
#         "uidb64": urlsafe_base64_encode(force_bytes(user.id)),
#     }
#     return reverse("password-reset-confirm", kwargs=kwargs)


# def normalise_email(email):
#     """
#     The local part of an email address is case-sensitive, the domain part
#     isn't.  This function lowercases the host and should be used in all email
#     handling.
#     """
#     clean_email = email.strip()
#     if "@" in clean_email:
#         local, host = clean_email.rsplit("@", 1)
#         return local + "@" + host.lower()
#     return clean_email
