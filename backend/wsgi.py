
import os
import sys

from django.core.wsgi import get_wsgi_application

from dj_static import Cling

path = '/backend'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = Cling(get_wsgi_application())
