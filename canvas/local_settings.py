import os
from django.core.urlresolvers import reverse_lazy

from .settings import BASE_DIR

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0']

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
