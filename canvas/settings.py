import os
import dj_database_url
import sentry_sdk
from urllib.parse import urlparse
from sentry_sdk.integrations.django import DjangoIntegration
from django.urls import reverse_lazy

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["CANVAS_KEY"]

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ["canvasreviews.herokuapp.com", "herokuapp.com"]


# Email settings
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = 587
    EMAIL_HOST_USER = os.environ["CANVAS_EMAIL_HOST_USER"]
    EMAIL_HOST_PASSWORD = os.environ["CANVAS_EMAIL_PW"]
    EMAIL_USE_TLS = os.environ["EMAIL_USE_TLS"]


# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "haystack",
    "storages",
    "elasticsearch",
    "gunicorn",
    "crispy_forms",
    "accounts",
    "reviews",
    "strains",
    "actions",
    "bootstrap3",
    "django_starfield",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "canvas.urls"
WSGI_APPLICATION = "canvas.wsgi.application"

ES_URL = urlparse(os.environ.get("BONSAI_URL") or "http://127.0.0.1:9200/")
HAYSTACK_CONNECTIONS = {
    "default": {
        "ENGINE": "haystack_elasticsearch5.Elasticsearch5SearchEngine",
        "URL": ES_URL.scheme + "://" + ES_URL.hostname + ":443",
        "INDEX_NAME": "haystack_reviews",
    },
}

if ES_URL.username:
    HAYSTACK_CONNECTIONS["default"]["KWARGS"] = {
        "http_auth": ES_URL.username + ":" + ES_URL.password
    }

HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
import dj_database_url

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}

DATABASES["default"] = dj_database_url.config()

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


CRISPY_TEMPLATE_PACK = "bootstrap4"


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Los_Angeles"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = "home"
LOGIN_REDIRECT_URL = reverse_lazy("reviews:reviews")
LOGOUT_REDIRECT_URL = "home"

# Static files
if os.environ.get("ENABLE_S3"):
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

    STATIC_URL = "https://%s/static/" % (AWS_S3_CUSTOM_DOMAIN)
    STATICFILES_STORAGE = "canvas.custom_storages.StaticRootS3BotoStorage"

    MEDIA_URL = "https://%s/media/" % (AWS_S3_CUSTOM_DOMAIN)
    DEFAULT_FILE_STORAGE = os.environ.get("DEFAULT_FILE_STORAGE")
    DEFAULT_FROM_EMAIL = os.environ.get("CANVAS_FROM_EMAIL")
else:
    STATICFILES_LOCATION = "static"
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]


sentry_sdk.init(dsn=os.environ.get("SENTRY_DSN"), integrations=[DjangoIntegration()])


if DEBUG:
    ALLOWED_HOSTS = []

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_CANVAS_NAME"),
            "USER": os.environ.get("DB_CANVAS_USER"),
            "PASSWORD": os.environ.get("DB_CANVAS_PW"),
            "HOST": "localhost",
            "PORT": "5432",
        }
    }

# Celery Configuration Options
CELERY_TIMEZONE = "US/Pacific"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
