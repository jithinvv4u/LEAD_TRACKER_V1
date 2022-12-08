"""
Settings specific to the development environment.

Setting those are specific to the development environment are
specified here. Common settings params are imported from the
base settings file.
"""
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

DEBUG = True

FRONT_ROOT_URL = ""

ENVIRONMENT = "development"
ALLOWED_HOSTS += ["*"]

CORS_ORIGIN_ALLOW_ALL = True


CORS_ORIGIN_WHITELIST = [
    "http://localhost:8100",
    "http://localhost:4200",
    "http://127.0.0.1",
]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Sentry settings

sentry_sdk.init(
    dsn=config.get("libs", "SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment=ENVIRONMENT,
)

# Media file settings for S3

AWS_ACCESS_KEY_ID = config.get("libs", "AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config.get("libs", "AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config.get("libs", "AWS_STORAGE_BUCKET_NAME")
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True
# AWS_DEFAULT_ACL = 'public'
DEFAULT_FILE_STORAGE = "s3_folder_storage.s3.DefaultStorage"
DEFAULT_S3_PATH = "media"
MEDIA_ROOT = "/%s/" % DEFAULT_S3_PATH
MEDIA_URL = "//%s.s3.amazonaws.com/media/" % AWS_STORAGE_BUCKET_NAME


FROM_EMAIL = ""
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = config.get("email", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("email", "EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

TIME_ZONE = "Asia/Calcutta"
