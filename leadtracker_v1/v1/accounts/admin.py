"""Admin file of the app accounts."""

import nested_admin

from django.utils.safestring import mark_safe

from django.contrib.auth.admin import UserAdmin
from fcm_django.models import FCMDevice

from django.conf import settings

from django.contrib import admin

from .models import ProjectUser
from .models import AccessToken
from .models import ValidationToken
from .models import UserDevice
from .models import Person
from .models import TermsAndConditions
from .models import UserTCAcceptance

environment = settings.ENVIRONMENT.capitalize()
admin.site.site_header = "%s leadtracker_v1 Admin" % environment
admin.site.site_title = "leadtracker_v1: %s Admin Portal" % (environment)
admin.site.index_title = "Welcome to leadtracker_v1 %s Portal" % (environment)


class ValidationTokenAdmin(admin.ModelAdmin):
    """Class view to customize validation token admin."""

    ordering = ("-updated_on",)

    def salt(self, obj):
        """Get salt."""
        return obj.idencode

    list_display = ("user", "key", "status", "salt", "type", "expiry")
    list_filter = ("type", "status")


class AccessTokenAdmin(admin.ModelAdmin):
    """Class view to customize validation token admin."""

    def email(self, obj):
        """Show email in list"""
        return obj.user.email

    list_display = ("user", "email", "key")


class UserDeviceAdmin(admin.ModelAdmin):
    """Class view to customize user device admin."""

    list_display = ("user", "device_id", "registration_id", "type")


class AccessTokenInline(admin.TabularInline):
    """In-line view function for SourceBatch."""

    def get_user_id(self, obj):
        return obj.user.idencode

    readonly_fields = ("get_user_id", "key", "created")
    model = AccessToken
    extra = 0


class UserAdmin(UserAdmin):
    """Overriding user adminto add additional fields"""

    readonly_fields = ("idencode",)
    ordering = ("-id",)
    inlines = [
        AccessTokenInline,
    ]

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            ("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "updated_email",
                    "dob",
                    "phone",
                    "address",
                    "language",
                    "image",
                    "idencode",
                )
            },
        ),
        (
            ("Internal values"),
            {
                "fields": (
                    "type",
                    "status",
                    "terms_accepted",
                    "privacy_accepted",
                    "email_verified",
                ),
            },
        ),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ("idencode", "first_name", "last_name", "email", "email_verified")



admin.site.register(ProjectUser, UserAdmin)
admin.site.register(UserDevice, UserDeviceAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(ValidationToken, ValidationTokenAdmin)
admin.site.register(Person)
admin.site.register(TermsAndConditions)
admin.site.register(UserTCAcceptance)
