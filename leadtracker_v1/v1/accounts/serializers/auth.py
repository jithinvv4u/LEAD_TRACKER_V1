"""Serializers related to the user model."""

from sentry_sdk import capture_exception

from rest_framework import serializers
from django.contrib.auth import authenticate

from common.exceptions import BadRequest
from common.exceptions import AccessForbidden
from common.exceptions import UnauthorizedAccess

from common.library import validate_password, decode

from v1.accounts.constants import VTokenTypeChoices

from v1.accounts import validator as accounts_validator

from v1.accounts.models import ProjectUser
from v1.accounts.models import ValidationToken

from v1.accounts.serializers import user as user_serializers


class ValidateUsernameSerializer(serializers.Serializer):
    """Serializer to check the username availability."""

    username = serializers.CharField()

    def to_representation(self, obj):
        """Overriding the value returned when returning th serializer."""
        response = accounts_validator.validate_username(obj["username"])
        return response


class ValidatePasswordSerializer(serializers.Serializer):
    """Serializer to check the password validity."""

    password = serializers.CharField()

    def to_representation(self, obj):
        """Overriding the value returned when returning th serializer."""
        response = {}
        response["valid"], response["message"] = validate_password(obj["password"])
        return response


class LoginSerializer(serializers.Serializer):
    """Serializer to login."""

    username = serializers.CharField()
    password = serializers.CharField()
    device_id = serializers.CharField(required=False)
    registration_id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def create(self, validated_data):
        """Overriding the create method."""
        user = authenticate(
            username=validated_data["username"], password=validated_data["password"]
        )
        if not user:
            raise UnauthorizedAccess("Invalid email or password")
        validated_data["user"] = user.id
        device_serializer = user_serializers.UserDeviceSerializer(data=validated_data)
        if device_serializer.is_valid():
            device_serializer.save()
        else:
            raise BadRequest(device_serializer.errors)
        return user

    def to_representation(self, obj):
        """Overriding the value returned when returning th serializer."""
        data = {
            "token": obj.issue_access_token(),
            "idencode": obj.idencode,
            "status": obj.status,
            "email_verified": obj.email_verified,
            "terms_accepted": obj.terms_accepted,
        }
        return data


class MagicLinkSerializer(serializers.Serializer):
    """Serializer to generate magic link and send email"""

    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        """Overriding create method to generate magic link and send email"""
        # TODO: change to try except

        user = ProjectUser.objects.filter(email=validated_data["email"]).first()
        if not user:
            raise BadRequest("User is not registered")
        user.generate_magic_link()
        return {"status": True, "message": "Magic link sent"}


class MagicLoginSerializer(serializers.Serializer):
    """Serializer to login with magic link."""

    validation_token = serializers.CharField()
    user_id = serializers.CharField()
    device_id = serializers.CharField()
    registration_id = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def create(self, validated_data):
        """Overriding the create method."""
        # TODO: change to validate_ method
        # TODO: change to not send user ID in link
        try:
            user_id = decode(validated_data["user_id"])
            token = ValidationToken.objects.get(
                user__id=user_id,
                key=validated_data["validation_token"],
                type=VTokenTypeChoices.VTOKEN_TYPE_MAGIC,
            )  # TODO: move to permission
            if token.is_valid:
                token.mark_as_used()
                user = token.user
                user.email_verified = True
                user.save()
                validated_data["user"] = user.id
                device_serializer = user_serializers.UserDeviceSerializer(
                    data=validated_data
                )
                if device_serializer.is_valid():
                    device_serializer.save()
                else:
                    raise BadRequest(device_serializer.errors)
            else:
                user = None
        except Exception as e:
            capture_exception(e)
            message = str(e)
            user = None
        if not user:
            raise AccessForbidden("Invalid link..")
        return user

    def to_representation(self, obj):
        """Overriding the value returned when returning th serializer."""
        data = {
            "token": obj.issue_access_token(),
            "id": obj.idencode,
            "status": obj.status,
            "email_verified": obj.email_verified,
            "terms_accepted": obj.terms_accepted,
        }
        return data
