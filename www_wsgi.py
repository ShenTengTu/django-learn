"""
Django WSGI configuration for deploying.

https://github.com/ShenTengTu/django-learn
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True)

home = os.path.expanduser("~")
project = "study_project"
path = '{}/projects/django-learn/{}'.format(home, project)
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = '{}.settings'.format(project)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
