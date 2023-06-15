import os
import ast
import warnings
import sentry_sdk
import datetime
import stripe

from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from pathlib import Path

from core.languages import LANGUAGES as CORE_LANGUAGES

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Tell Django about the custom `User` model we created. The string
# `account.User` tells Django we are referring to the `CustomUser` model in
# the `account` module. This module is registered above in a setting
# called `INSTALLED_APPS`.
AUTH_USER_MODEL = "account.CustomUser"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.environ.get("SECRET_KEY"))
RSA_PRIVATE_KEY = os.environ.get("RSA_PRIVATE_KEY", None)
RSA_PRIVATE_PASSWORD = os.environ.get("RSA_PRIVATE_PASSWORD", None)
JWT_MANAGER_PATH = os.environ.get(
    "JWT_MANAGER_PATH", "djolowin.core.jwt_manager.JWTManager"
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [
    "*",
]


SITE_ID = 1
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # Third party apps
    "celery",
    "corsheaders",
    "django_countries",
    "django_extensions",
    "django_filters",
    "graphene_django",
    "graphql_auth",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "phonenumber_field",
    "rest_framework",
    "rest_framework.authtoken",
    "social_django",
    # local apps
    "account",
    "analytics",
    "app_currency",
    "auction",
    "base",
    "bundle",
    "channel",
    "collection",
    "communication",
    "core",
    "djolowin_graphql",
    "djolowin_profile",
    "order",
    "permission",
    "playercard",
    "reward",
    "transaction",
    "wallet",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "djolowin.urls"


context_processors = [
    "communication.notifications.context_processors.notifications",
    "wallet.context_processors.user_balance",
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "social_django.context_processors.backends",
    "social_django.context_processors.login_redirect",
]
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": context_processors,
        },
    },
]

WSGI_APPLICATION = "djolowin.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": str(os.environ.get("DB_NAME")),
        "USER": str(os.environ.get("DB_USER")),
        "PASSWORD": str(os.environ.get("DB_PASSWORD")),
        "HOST": str(os.environ.get("DB_HOST")),
        "PORT": str(os.environ.get("DB_PORT")),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# JWT settings
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}


AUTHENTICATION_BACKENDS = [
    "graphql_auth.backends.GraphQLAuthBackend",
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.google.GoogleOAuth2",
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = CORE_LANGUAGES

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"# URL that handles the media
# served \from MEDIA_ROOT. Make sure to use a
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = "/static/"
DJOLOWIN_STATIC_BASE_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGOUT_REDIRECT_URL = "account:login"
LOGIN_REDIRECT_URL = "base:home"
LOGIN_URL = "account:login"
LOGOUT_URL = "account:logout"

APPEND_SLASH = True
DJOLOWIN_ACCOUNTS_REDIRECT_URL = "account:user-detail"

# Defaults variables\
DATABASE_CONNECTION_DEFAULT_NAME = os.environ.get("DB_NAME")
DEFAULT_FROM_EMAIL = "monsieurdjolo@djolo.win"
DEFAULT_CURRENCY = "cad"
DEFAULT_CURRENCY_CODE_LENGTH = 3
DEFAULT_DECIMAL_PLACES = 2
DEFAULT_MAX_DIGITS = 12
DEFAULT_CURRENCY_CODE_LENGTH = 3
DJOLOWIN_PLAYERCARD_PAGINATE_BY = 8
DJOLOWIN_NOTIFICATIONS_PER_PAGE = 20
DJOLOWIN_SAVE_SENT_EMAILS_TO_DB = True

# Email server configuration
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp-mail.outlook.com"
EMAIL_HOST_USER = "monsieurdjolo@djolo.win"
EMAIL_HOST_PASSWORD = "Emmanuel225##"


# Password reset settings
# Number of days a password reset link is valid
PASSWORD_RESET_TIMEOUT_DAYS = 1

# Email subject for password reset emails
PASSWORD_RESET_SUBJECT = "Reset your password on DjoloWin"

# Email body for password reset emails
PASSWORD_RESET_EMAIL_TEMPLATE = "djolowin/account/password_reset_email.html"

EMAIL_TEMPLATE_NAME = "djolowin/account/password_reset_email.html"

# Stripe settings for payment gateway
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")
stripe.api_key = STRIPE_SECRET_KEY

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
]
CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_WHITELIST = ("http://localhost:8080",)

JWT_EXPIRE = 60 * 60 * 24 * 7  # 7 days


# Celery settings for background tasks
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_RESULT_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"


# GraphQL settings
GRAPHENE = {
    "SCHEMA": "djolowin_graphql.api.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
    "ATOMIC_MUTATIONS": True,
}

GRAPHQL_JWT = {
    # ...
    "JWT_ALLOW_ANY_CLASSES": [
        "graphql_auth.mutations.Register",
        "graphql_auth.mutations.VerifyAccount",
        "graphql_auth.mutations.ResendActivationEmail",
        "graphql_auth.mutations.SendPasswordResetEmail",
        "graphql_auth.mutations.PasswordReset",
        "graphql_auth.mutations.ObtainJSONWebToken",
        "graphql_auth.mutations.VerifyToken",
        "graphql_auth.mutations.RefreshToken",
        "graphql_auth.mutations.RevokeToken",
        "graphql_auth.mutations.VerifySecondaryEmail",
    ],
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
}

ENABLE_SSL = False

# SOcial auth settings
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GOOGLE_CLIENT_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GOOGLE_SECRET_KEY")
SOCIAL_AUTH_PIPELINE = [
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
    "account.social_auth.create_user",
]
