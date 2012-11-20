import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'med_alliance.settings.producao'

path = '/home/ubuntu/med_alliance'
if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

