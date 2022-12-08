"""Filters used in the app accounts."""

from django_filters import rest_framework as filters

from v1.accounts.models import ProjectUser


class UserFilter(filters.FilterSet):
    """
    Filter for ProjectUser.
    """

    email = filters.CharFilter()

    class Meta:
        model = ProjectUser
        fields = ["email"]
