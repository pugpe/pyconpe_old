import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{{ mysql_database }}',
        'USER': '{{ mysql_user }}',
        'PASSWORD': '{{ mysql_password }}',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
               "init_command": "SET storage_engine=INNODB",
        },

    }
}

if 'test' in sys.argv:
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':  os.path.join(PROJECT_ROOT, 'banco.sqlite')
        },

    }



# Use sua conta do gmail
DEFAULT_FROM_EMAIL = 'PyCon PE <sample@gmail.com>'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'sample@gmail.com'
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587

INTERNAL_IPS = [
    "127.0.0.1",
]
