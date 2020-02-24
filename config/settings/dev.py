from config.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DATABASE_NAME', 'eclass'),
        'HOST': os.environ.get('DATABASE_HOST', '127.0.0.1'),
        'USER': os.environ.get('DATABASE_USER', 'eclass'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD', 'eclass'),
        'PORT': '5432',
    }
}