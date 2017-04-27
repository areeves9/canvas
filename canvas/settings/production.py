import os
from .base import *

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = False

ADMINS = (
    ('Andrew R.', 'areeves9@icloud.com')
)

ALLOWED_HOSTS = ['https://infinite-gorge-34857.herokuapp.com/']

DATABSES = {
    'default': {}
}

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

INSTALLED_APPS += [
'bootstrap3',
'storages',
'gunicorn',
]

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME')

AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
