"""
Settings specific to the production environment.

Setting those are specific to the production environment are
specified here. Common settings params are imported from the
base settings file.
"""
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from .base import *

ENVIRONMENT = "production"

FRONT_ROOT_URL = ""
ALLOWED_HOSTS += []


CORS_ORIGIN_WHITELIST = []

INSTALLED_APPS += [
    "django_otp",
    "django_otp.plugins.otp_totp",
]

MIDDLEWARE += [
    # MFA OTP
    "django_otp.middleware.OTPMiddleware"
]

# Sentry settings

sentry_sdk.init(
    dsn=config.get("libs", "SENTRY_DSN"),
    integrations=[DjangoIntegration()],
    environment=ENVIRONMENT,
)

# REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = [
#     'rest_framework.throttling.AnonRateThrottle',
#     'rest_framework.throttling.UserRateThrottle'
# ]
# REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
#     'anon': '5/min',
#     'user': '50000/day'
# }

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

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

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_SSL = False
EMAIL_HOST = "smtp.sparkpostmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = config.get("email", "EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config.get("email", "EMAIL_HOST_PASSWORD")
FROM_EMAIL = ""
EMAIL_USE_TLS = True

TIME_ZONE = "UTC"
