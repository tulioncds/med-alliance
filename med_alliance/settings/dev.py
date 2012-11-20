from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'med_alliance',
        'USER': 'med_alliance_user',
        'PASSWORD': 'med_alliance31',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
