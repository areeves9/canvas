import os
from .base import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = os.environ.get('CANVAS_KEY')
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'canvas',
        'USER': 'toker',
        'PASSWORD': os.environ['DB_CANVAS_PW'],
        'HOST': 'localhost',
        'PORT': '5432',

    }
}


STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join("reviews", "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, "static_production")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media_production")

LOGIN_URL = reverse_lazy('auth:login')
LOGIN_REDIRECT_URL = reverse_lazy('accounts:profile')
