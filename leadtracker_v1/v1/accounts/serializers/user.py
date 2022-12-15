"""Serializers related to the user model."""

from rest_framework import serializers
from django.contrib.auth import authenticate

from common.exceptions import BadRequest
from common.exceptions import AccessForbidden

from common.drf_custom import fields as custom_fields
from common.drf_custom.mixins import WriteOnceMixin

from common.library import validate_password, decode
from common.library import pop_out_from_dictionary

from v1.accounts.models import ProjectUser
from v1.accounts.models import Person
from v1.accounts.models import UserDevice
from v1.accounts.models import TermsAndConditions

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserSerializer(WriteOnceMixin, serializers.ModelSerializer):
    """Serializer for user."""

    id = custom_fields.IdencodeField(read_only=True)
    first_name = serializers.CharField()
    email = serializers.CharField()  # TODO: change to write_once field
    status = serializers.IntegerField(required=False)

    terms_accepted = serializers.BooleanField(required=False)
    privacy_accepted = serializers.BooleanField(required=False)
    email_verified = serializers.BooleanField(required=False)
    password = serializers.CharField(write_only=True)

    class Meta:
        """Meta info."""

        model = ProjectUser
        fields = [
            "id",
            "first_name",
            "email",
            "password",
            "terms_accepted",
            "privacy_accepted",
            "email_verified",
            "status",
        ]

        write_once_fields = ("password")

    def validate_username(self, value):
           """Function to validate username."""
           value = value.lower()
           try:
               validate_email(value)
           except ValidationError:
               raise serializers.ValidationError(_('Invalid Email ID.'))
           else:
               if ProjectUser.objects.filter(username=value).exists():
                   raise serializers.ValidationError(_('Email already taken'))
           return value
       
    def update_password(self, instance, validated_data):
        """Function to update password"""
        if not "current_password" in validated_data.keys():
            raise BadRequest("Old password is required to update password")
        if not authenticate(
            username=instance.email, password=validated_data["current_password"]
        ):
            raise AccessForbidden("Old password supplied is wrong")
        valid, errors = validate_password(validated_data["new_password"])
        if not valid:
            raise BadRequest(errors)
        instance.set_password(validated_data["new_password"])
        instance.save()
        return True

    def update(self, instance, validated_data):
        """
        Overriding default update method.

        Update user details and the django user details..
        """
        if "email" in validated_data.keys():
            self.update_email(instance, validated_data)
            validated_data.pop("email")

        if "new_password" in validated_data.keys():
            self.update_password(instance, validated_data)
            pop_out_from_dictionary(
                validated_data, ["current_password", "new_password"]
            )
        super(UserSerializer, self).update(instance, validated_data)
        return instance

    def create(self, validated_data):
        """Overriding the create method."""
        self.validate_username(validated_data["email"])
        # TODO: move to validate_
        if not "username" in validated_data.keys() or not validated_data["username"]:
            validated_data["username"] = validated_data["email"]
        validated_data["first_name"] = validated_data["first_name"].title()
        # validated_data["last_name"] = validated_data["last_name"].title()
        extra_keys = list(
            set([field.name for field in ProjectUser._meta.get_fields()])
            ^ set([*validated_data])
        )

        pop_out_from_dictionary(validated_data, extra_keys)
        user = ProjectUser.objects.create(**validated_data)
        if "password" in validated_data.keys():
            user.set_password(validated_data["password"])
            user.save()
        # if self.context.get("view", None):
            # user.verify_email()  # TODO: change to a context variable

        return user


class UserListSerializer(serializers.ModelSerializer):
    """Serializer for user."""

    # TODO: combine to user details serializer using min mode
    id = custom_fields.IdencodeField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    phone = custom_fields.PhoneNumberField(required=False, allow_blank=True)
    image = custom_fields.RemovableImageField(required=False, allow_blank=True)

    class Meta:
        """Meta info."""

        model = ProjectUser
        fields = ["id", "first_name", "email"]


class UserDeviceSerializer(WriteOnceMixin, serializers.ModelSerializer):
    """Serializer of user device model."""

    id = serializers.SerializerMethodField()  # TODO: change to idencode field

    class Meta:
        """Meta info."""

        model = UserDevice
        fields = "__all__"
        extra_kwargs = {
            "device_id": {"required": True},
            "creator": {"write_only": True},
            "updater": {"write_only": True},
            "user": {"write_only": True},
        }

    def get_id(self, obj):
        """Get encoded  id."""
        return obj.idencode

    def create(self, validated_data):
        """Overriding the create method."""
        for device in UserDevice.objects.filter(device_id=validated_data["device_id"]):
            if device.user.type == validated_data["user"].type:
                device.active = False
                device.updater = validated_data["user"]
                device.save()

        try:
            device = UserDevice.objects.get(
                device_id=validated_data["device_id"], user=validated_data["user"]
            )
            device.registration_id = validated_data.get(
                "registration_id", device.registration_id
            )
            device.type = validated_data.get("type", device.type)
            device.name = validated_data.get("name", device.name)
            device.updater = validated_data["user"]
            device.active = True
            device.save()
            return device
        except:
            device = UserDevice.objects.create(**validated_data)
            return device


class AbstractPersonSerializer(serializers.ModelSerializer):
    """Serializer for Abstract Person model"""

    id = custom_fields.IdencodeField(read_only=True)

    class Meta:
        abstract = True
        fields = (
            "first_name",
            "last_name",
            "gender",
            "dob",
            "birth_city",
            "marital_status",
            "email",
            "phone",
        )


class PersonSerializer(AbstractPersonSerializer):
    """Serializer for Person model"""

    id = custom_fields.IdencodeField(read_only=True)
    phone = custom_fields.PhoneNumberField(required=False, allow_blank=True)

    class Meta:
        model = Person
        fields = (
            "first_name",
            "last_name",
            "gender",
            "dob",
            "birth_city",
            "marital_status",
            "email",
            "phone",
        )

    @staticmethod
    def has_changed(instance, field_name, value):
        return not getattr(instance, field_name) == value

    def get_changed_fields(instance, validated_data):
        field_titles = {
            "first_name": "contact info",
            "last_name": "contact info",
            "gender": "contact info",
            "dob": "contact info",
            "birth_city": "contact info",
            "marital_status": "contact info",
            "email": "contact info",
            "phone": "contact info",
            "image": "image",
        }
        changed_fields = []
        for field_name, value in validated_data.items():
            if PersonSerializer.has_changed(instance, field_name, value):
                changed_fields.append(field_titles.get(field_name, ""))
        return list(set(changed_fields))


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsAndConditions
        fields = ("title", "version")
