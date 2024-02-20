from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': str(os.getenv("PGDATABASE")),
        'USER': str(os.getenv("PGUSER")),
        'PASSWORD': str(os.getenv("PGPASSWORD")),
        'HOST': str(os.getenv("PGHOST")),
        'PORT': str(os.getenv("PGPORT")),
    }
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

ALLOWED_HOSTS = [
    'localhost'
]
