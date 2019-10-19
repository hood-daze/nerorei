# localではenvは使わない感じ
from .base import *

#####################
# Security settings #
#####################

DEBUG = True

SECRET_KEY = '<fake-secret-key>'

ALLOWED_HOSTS = ['*']

############
# Database #
############

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

################
# Static files #
################
# 開発時の検証で上書きしている
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')

################
# Email setting #
################
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Whether to send SMTP 'Date' header in the local time zone or in UTC.
EMAIL_USE_LOCALTIME = False

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Email address that error messages come from.
SERVER_EMAIL = 'root@localhost'
