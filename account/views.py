from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views import generic, View
from django.views.generic import DetailView, RedirectView, UpdateView

from .forms import UserRegistrationForm, UserUpdateForm
from .mixins import CustomDispatchMixin
from .tokens import account_activation_token
from .decorators import user_is_active
from .signals import user_signed_up

User = get_user_model()


USER_MODEL_MISMATCH = """
The registration view ({view}) is using the form class {form},
but the model used by the form ({form_model}) is not your Django installation's user model ({user_model}).
Please use a custom registration form class compatible with your custom user model.
See django-registration's documentation on custom user models for more details.
"""

class EmailSentView(View):
    def get(self, request):
        user = request.user
        email = user.email
        return render(request, "djolowin/account/verification_email_sent.html", {"email": email})

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = (urlsafe_base64_decode(uidb64).decode())
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            # Log the user in, redirect to their dashboard, or show a success message
            messages.success(request, "Your account has been successfully verified. You can now login.")
            return redirect("account:login")
        else:
            # Display an 'Invalid activation link' error message
            return render(request, "account/activation_invalid.html")


class SignupView(CustomDispatchMixin, generic.CreateView):
    form_class = UserRegistrationForm
    success_url = reverse_lazy("account:signup-done")
    template_name = "djolowin/account/signup.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            user_signed_up.send(sender=self.__class__, user=user, request=request)
            mail_subject = "Activate your account."
            message = render_to_string(
                "djolowin/account/activation_email.html",
                {   "from_email": settings.DEFAULT_FROM_EMAIL,
                    "protocol": "http",
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return render (request, "djolowin/account/verification_email_sent.html", {"email": to_email})
        return render(request, self.template_name, {"form": form})


user_signup_view = SignupView.as_view()


class CustomLoginView(CustomDispatchMixin, LoginView):
    template_name = "djolowin/account/login.html"
user_login_view = CustomLoginView.as_view()


class RequestActivationEmailView(View):
    template_name = "djolowin/account/request_activation_email.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()

        if user and not user.is_active:
            # Generate the token
            token = account_activation_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Send the activation email
            subject = "Activate your account"
            message = render_to_string(
                "djolowin/account/activation_email.html",
                {
                    "user": user,
                    "domain": request.get_host(),
                    "uid": uid,
                    "token": token,
                },
            )
            email = EmailMessage(subject, message, to=[user.email])
            email.send()

            messages.success(request, "Activation email sent. Please check your inbox.")
            return redirect("account:email_sent")

        messages.error(request, "Email not found or the account is already activated.")
        return render(request, self.template_name)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "djolowin/account/user/user_detail.html"
    fields = [
        "username",
        "email",
        "first_name",
        "last_name",
        "country",
        "profile_img",
        "date_joined",
    ]

    def get_object(self, queryset=None):
        return self.request.user


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "djolowin/account/user/user_form.html"
    model = User
    form_class = UserUpdateForm
    success_message = _("Your account information has been successfully updated")

    def get_success_url(self):
        session_user = self.request.user
        assert (
            session_user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return session_user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse_lazy(
            settings.DJOLOWIN_ACCOUNTS_REDIRECT_URL,
            kwargs={"username": self.request.user.username},
        )


user_redirect_view = UserRedirectView.as_view()
