import os

from .settings import BASE_DIR

ALLOWED_HOSTS = []

HAYSTACK_CONNECTIONS = {
       'default': {
           'ENGINE': 'haystack_elasticsearch5.Elasticsearch5SearchEngine',
           'URL': 'http://127.0.0.1:9200/',
           'INDEX_NAME': 'haystack_reviews',
       },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_CANVAS_NAME'],
        'USER': os.environ['DB_CANVAS_USER'],
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
