import os
import sys

ROOT = os.path.dirname(__file__)
PARENT = os.path.dirname(ROOT)

if PARENT not in sys.path:
    sys.path.append(PARENT)

if ROOT not in sys.path:
    sys.path.append(ROOT)

os.environ['DJANGO_SETTINGS_MODULE'] = 'philly_legislative.settings'

import django.core.handlers.wsgi
djangoapplication = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    if 'SCRIPT_NAME' in environ:
        del environ['SCRIPT_NAME']
    return djangoapplication(environ, start_response)
