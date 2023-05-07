from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import (
    user_detail_view,
    user_signup_view,
    user_update_view,
    user_redirect_view,
    user_login_view,
    RequestActivationEmailView,
    ActivateAccountView,
    EmailSentView,
)

app_name = "account"

urlpatterns = [
    path("login/", view=user_login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", view=user_signup_view, name="signup"),
    path("activate/<uidb64>/<token>/", ActivateAccountView.as_view(), name="activate"),
    path(
        "request_activation_email/",
        RequestActivationEmailView.as_view(),
        name="request_activation_email",
    ),
    path("email_sent/", EmailSentView.as_view(), name="email_sent"),
    path("redirect/", view=user_redirect_view, name="user-redirect"),
    path("update/", view=user_update_view, name="user-update"),
    path("user-detail/<str:username>", view=user_detail_view, name="user-detail"),
    # Password change urls
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(
            template_name="djolowin/account/password_change_form.html",
            success_url="done/",
        ),
        name="password-change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="djolowin/account/password/password_change_done.html"
        ),
        name="password-change-done",
    ),
    # reseT password urls
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="djolowin/account/password/password_reset_form.html",
            email_template_name="djolowin/account/password/password_reset_email.html",
            success_url="sent/",
        ),
        name="password-reset",
    ),
    path(
        "password-reset/sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="djolowin/account/password/password_reset_email_sent.html"
        ),
        name="password-reset-sent",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy("account:password-reset-complete"),
            template_name="djolowin/account/password/password_reset_confirm.html",
        ),
        name="password-reset-confirm",
    ),
    path(
        "password-reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="djolowin/account/password/password_reset_complete.html"
        ),
        name="password-reset-complete",
    ),
]
