from .base import *
import os

SECRET_KEY = os.environ.get['SECRET_KEY']
DEBUG = False

ADMINS = (
    ('Andrew R.', 'areeves9@icloud.com')
)

ALLOWED_HOSTS = ['https://infinite-gorge-34857.herokuapp.com/', 'herokuapp.com']

import dj_database_url
DATABASES['default'] =  dj_database_url.config()

INSTALLED_APPS += [
'bootstrap3',
'storages',
'gunicorn',
]

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']

AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME

STATIC_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


# STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join("reviews", "static")
# ]
#
# STATIC_ROOT = os.path.join(BASE_DIR, "static_production")
#
# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, "media_production")
