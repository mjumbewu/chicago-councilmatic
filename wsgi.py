import os
import sys

ROOT = os.path.dirname(__file__)
CM = os.path.join(ROOT, 'councilmatic')

if ROOT not in sys.path:
    sys.path.append(ROOT)

if CM not in sys.path:
    sys.path.append(CM)

os.environ['DJANGO_SETTINGS_MODULE'] = 'councilmatic.settings'

import django.core.handlers.wsgi
djangoapplication = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    if 'SCRIPT_NAME' in environ:
        del environ['SCRIPT_NAME']
    return djangoapplication(environ, start_response)
    
if __name__ == '__main__':
    from wsgiref.util import setup_testing_defaults
    from wsgiref.simple_server import make_server

    httpd = make_server('', 1337, application)
    print "Serving on port 1337..."
    httpd.serve_forever()
