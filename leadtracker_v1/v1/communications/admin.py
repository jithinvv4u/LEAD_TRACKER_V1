"""Django admin manager of the app communications."""

from django.contrib import admin

from v1.accounts.models import ProjectUser

from v1.accounts.constants import UserTypeChoices

from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    """Class view to customize Notification admin."""

    list_display = (
        "user",
        "title_en",
        "type",
        "event",
        "action",
        "is_read",
    )
    list_filter = (
        "type",
        "event",
        "action",
    )

    def get_queryset(self, request):
        """Query set to list objects."""
        queryset = super().get_queryset(request)
        try:
            if request.user.type != UserTypeChoices.USER_TYPE_ADMIN:
                queryset = queryset.filter(user=request.user)
        except:
            pass
        return queryset


admin.site.register(Notification, NotificationAdmin)
