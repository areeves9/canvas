import os
from .base import *


# SECRET_KEY = '_y2&=f+fz%yvf&^zdq#-1%!47-7(6n8)kmt(c*1l92&=_bmm&x'
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
DEBUG = False

ADMINS = (
    ('Andrew R.', 'areeves9@icloud.com')
)

# ALLOWED_HOSTS = ['https://infinite-gorge-34857.herokuapp.com/']
ALLOWED_HOSTS = ['infinite-gorge-34857.herokuapp.com']


DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}

import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
DATABASES['default'] = dj_database_url.config(default='postgres://fmsdkzturgvwyo:f761c48073d4188f93a089a833a31b5476794e246295b58c7927068ef370dcbc@ec2-54-225-119-223.compute-1.amazonaws.com:5432/d2q3ilnf3mei2b')

# DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}



INSTALLED_APPS += [
'storages',
'gunicorn',
]

DEFAULT_FILE_STORAGE = "storages.backends.s3boto.S3BotoStorage"
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', '')

# AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
# STATIC_URL = "https://" + AWS_STORAGE_BUCKET_NAME + ".s3.amazonaws.com/"
# MEDIA_URL = STATIC_URL + "media/"
#
# STATICFILES_DIRS = ( os.path.join(BASE_DIR, "static"))
# STATIC_ROOT = "staticfiles"
#
#
#
#
# STATICFILES_STORAGE = "storages.backends.s3boto.S3BotoStorage"
#
#
# STATIC_ROOT = STATIC_URL
