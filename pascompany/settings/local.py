from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'pascompany',
        'USER': 'pascompany',
        'PASSWORD': 'pascompany',
        'PORT': '5432',
        'HOST': 'localhost'
    }
}