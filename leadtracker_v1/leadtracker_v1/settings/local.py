"""
Settings specific to the local environment.

Setting those are specific to the local environment are
specified here. Common settings params are imported from the
base settings file.
"""

from .base import *

DEBUG = True

FRONT_ROOT_URL = "http://localhost:8080"

INSTALLED_APPS += []

ALLOWED_HOSTS += ['127.0.0.1']

MIDDLEWARE += []

CORS_ORIGIN_WHITELIST = [
    "http://localhost",
    "http://127.0.0.1",
]

ENVIRONMENT = "local"

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config.get("database", "DB_NAME"),
        "USER": config.get("database", "DB_USER"),
        "PASSWORD": config.get("database", "DB_PASSWORD"),
        "PORT": "5432",
        "HOST": "localhost",
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")


FROM_EMAIL = ""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = config.get("email", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("email", "EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

TIME_ZONE = "Asia/Calcutta"
