"""Serializers related to handling notifications."""


from rest_framework import serializers

from common.drf_custom import fields as custom_fields

from v1.communications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer to manage notification."""

    id = serializers.SerializerMethodField()

    class Meta:
        """Meta info."""

        model = Notification
        exclude = ("send_to",)

        extra_kwargs = {
            "creator": {"write_only": True},
            "updater": {"write_only": True},
            "devices": {"write_only": True},
            "action": {"write_only": True},
            "action_url": {"write_only": True},
            "user": {"write_only": True},
        }

    def get_id(self, obj):
        """Get encoded  id."""
        return obj.idencode
