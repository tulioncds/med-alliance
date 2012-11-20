from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'med_alliance',
        'USER': 'med_alliance_user',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'bootstrapform',
    'tastypie',
    'base',
    'core',
    'south',
    'schedule',
    'django.contrib.admin',
    'requests',
    'pagseguro2',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/ubuntu/med_alliance/media/'
STATIC_URL = '/static/'
STATIC_ROOT = '/home/ubuntu/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

LOGIN_URL = '/'
LOGIN_REDIRECT_URL = '/home'

FABRIC = {
       'IP' : '54.245.43.222',
       'HOME' : '/home/ubuntu/',
       'CODE_ROOT' : '/home/ubuntu/med_alliance',
       'PROJETO' : 'med_alliance',
       'USER' : 'ubuntu',
}
