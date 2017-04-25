from .base import *
import os
import dj_database_url

DEBUG = False

ADMINS = (
    ('Andrew R.', 'areeves9@icloud.com')
)

ALLOWED_HOSTS = ['https://cryptic-forest-89537.herokuapp.com/', 'herokuapp.com']

DATABASES = {
    'default': {}
}

DATABASES['default'] =  dj_database_url.config()

AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
SECRET_KEY = os.environ['SECRET_KEY']
