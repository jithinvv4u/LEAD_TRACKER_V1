"""Filters used in the app products."""

from django_filters import rest_framework as filters

from django.db.models import Q

from common.exceptions import BadRequest

from common import library as comm_lib

from v1.communications.models import Notification


class NotificationFilter(filters.FilterSet):
    """
    Filter for Notifications.
    """

    search = filters.CharFilter(method="search_fields")

    class Meta:
        model = Notification
        fields = [
            "search",
        ]

    def search_fields(self, queryset, name, value):
        return queryset.filter(title_en__icontains=value)
