"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv
from django.core.wsgi import get_wsgi_application
from pathlib import Path
import os

env_file_path =  Path(__file__).resolve().parent.parent
dotenv_path = os.path.join(env_file_path, ".env")
load_dotenv(dotenv_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", str(os.getenv("SETTINGS_MODULE")))
application = get_wsgi_application()
