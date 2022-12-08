"""All custom used fields are declared here."""

# from django.contrib.auth.hashers import make_password
import copy
import json

from rest_framework import serializers
from openpyxl import load_workbook

from common.library import encode
from common.library import unix_to_datetime
from common.library import decode
from common.library import validate_phone
from common.library import split_phone
from common.library import validate_password


class UnixTimeField(serializers.DateTimeField):
    """Custom field to accept Unix time stamp in date time field."""

    def to_internal_value(self, data):
        """Function to convert date time from Unix."""
        return unix_to_datetime(data)


class PasswordField(serializers.CharField):
    """Custom field for password."""

    write_only = True
    allow_null = False

    def to_internal_value(self, value):
        """Validator to validate password."""
        valid, messages = validate_password(value)
        if not (valid):
            raise serializers.ValidationError(messages)
        return value


class PhoneNumberField(serializers.CharField):
    """
    Custom field for phone number.

    Input can be in any of the formats
        - dict {'dial_code':'+1', 'phone':'81818181818'}
        - list ['+1', '81818181818']
        - tuple ('+1', '81818181818')
        - str '+181818181818'
    Output can be formatted as a dict, list or str.

    The format is by default a dict.
    """

    output_format = dict  # Supports dict, str or list
    supported_formats = [str, list, dict]

    def __init__(self, output_format=dict, **kwargs):
        """Initializing PhoneNumberField object, to set output_format"""
        if output_format not in self.supported_formats:
            raise ValueError(
                "output_format not supported. It should be " "either dict, str or list."
            )
        self.output_format = output_format
        super(PhoneNumberField, self).__init__(**kwargs)

    def format(self, code, phone):
        """
        Function to format the output according to specified output format
        """
        if self.output_format == dict:
            phone_number = {"dial_code": code, "phone": phone}
        elif self.output_format == list:
            phone_number = [code, phone]
        else:
            phone_number = "%s%s" % (code, phone)
        return phone_number

    def to_internal_value(self, value):
        """Validator to validate phone."""
        if type(value) == dict:

            if (not value["dial_code"] or not value["phone"]) and self.allow_blank:
                return ""

            if "dial_code" not in value.keys() or "phone" not in value.keys():
                raise serializers.ValidationError("Invalid phone number/country code")
            phone = "%s%s" % (value["dial_code"], value["phone"])
        elif type(value) == str:
            phone = value
        elif type(value) in [tuple, list]:
            phone = "".join(value)
        else:
            raise serializers.ValidationError("Un-supported phone number format")

        if not phone and self.allow_blank:
            return ""

        if not phone.startswith("+"):
            phone = "+%s" % phone
        phone = validate_phone(phone)
        if not phone:
            raise serializers.ValidationError("Invalid phone number/country code")
        return phone

    def to_representation(self, value):
        """Validator to validate phone."""
        code, phone = split_phone(value)
        return self.format(code, phone)


class CharListField(serializers.CharField):
    """Custom field for character list field."""

    child = serializers.CharField()

    def to_representation(self, value):
        """Validator to validate phone."""
        try:
            return eval(value)
        except:
            return value

    def to_internal_value(self, value):
        """Validator to validate phone."""
        try:
            return eval(value)
        except:
            return value


class JsonField(serializers.CharField):
    """Custom field for character list field."""

    child = serializers.CharField()

    def to_representation(self, value):
        """Validator to validate phone."""
        try:
            return json.loads(value)
        except:
            return value

    def to_internal_value(self, value):
        """Validator to validate phone."""
        try:
            return json.dumps(value)
        except:
            return value


class IdencodeField(serializers.CharField):
    """Encoded id field."""

    serializer = None
    related_model = None

    def __init__(self, serializer=None, related_model=None, *args, **kwargs):
        """Initializing field object."""
        self.serializer = serializer
        self.related_model = related_model
        super(IdencodeField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Override the returning method.

        This function will check if the serializer is supplied
        in case of foreign key field. In case of foreign key, the
        value will be and object. If it is  normal id then it is
        going to be type int.
        """
        if not value:
            return None
        if self.serializer:
            return self.serializer(value).data
        if isinstance(value, int):
            return encode(value)
        try:
            return encode(value.id)
        except:
            return None

    def to_internal_value(self, value):
        """To convert value for saving."""
        if self.related_model and isinstance(value, self.related_model):
            return value
        try:
            value = int(value)
        except:
            value = decode(value)
        if not value:
            raise serializers.ValidationError("Invalid id/pk format")
        related_model = self.related_model
        if not related_model:
            try:
                related_model = self.parent.Meta.model._meta.get_field(
                    self.source
                ).related_model
            except:
                raise serializers.ValidationError(
                    "Invalid key, the key should be same as the model. "
                )
        try:
            return related_model.objects.get(id=value)
        except:
            raise serializers.ValidationError("Invalid pk - object does not exist.")


class ManyToManyIdencodeField(serializers.CharField):
    """Encoded id field."""

    serializer = None
    related_model = None

    def __init__(self, serializer=None, related_model=None, *args, **kwargs):
        """Initializing field object."""
        self.serializer = serializer
        self.related_model = related_model
        super(ManyToManyIdencodeField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Override the returning method.

        This function will check if the serializer is supplied
        in case of foreign key field. In case of foreign key, the
        value will be and object. If it is  normal id then it is
        going to be type int.
        """
        if not value:
            return None
        if self.serializer:
            data = []
            for pk in value.all():
                data.append(self.serializer(pk).data)
            return data
        data = []
        for item in value.all():
            if isinstance(item, int):
                data.append(encode(item))
            try:
                data.append(encode(item.id))
            except:
                return None
        return data

    def to_internal_value(self, value):
        """To convert value for saving."""
        data = []
        for pk in value:
            try:
                data.append(int(pk))
            except:
                data.append(decode(pk))
        related_model = self.related_model
        if not related_model:
            try:
                related_model = self.parent.Meta.model._meta.get_field(
                    self.source
                ).related_model
            except:
                raise serializers.ValidationError(
                    "Invalid key, the key should be same as the model. "
                )
        try:
            return related_model.objects.filter(id__in=data)
        except:
            raise serializers.ValidationError("Invalid pk - object does not exist.")


class RemovableImageField(serializers.ImageField, serializers.CharField):
    """
    DRF does not give you an option to remove an image, Since emtpy values are
    not accepted by the ImageField.
    However, if an empty value is passed for the field in serializer update, the
    image id correctly removed.
    This field does just that
    """

    def to_internal_value(self, data):
        """Return emtpy string if input is an empty string"""
        if not data:
            return data
        return super(serializers.ImageField, self).to_internal_value(data)


class BulkTemplateField(serializers.FileField):
    excel_template = None

    def __init__(self, excel_template, *args, **kwargs):
        super(BulkTemplateField, self).__init__(*args, **kwargs)
        self.excel_template = excel_template

    def to_internal_value(self, data):
        file = super(BulkTemplateField, self).to_internal_value(data)

        wb = load_workbook(file, data_only=True)
        excel = self.excel_template(workbook=wb)
        return excel.validate()


class KWArgsObjectField(serializers.Field):
    """Encoded id field."""

    serializer = None
    related_model = None

    def __init__(self, serializer=None, related_model=None, *args, **kwargs):
        """Initializing field object."""
        self.serializer = serializer
        self.related_model = related_model
        super(KWArgsObjectField, self).__init__(*args, **kwargs)

    def get_value(self, dictionary):
        """Overriding the get value of the serializer field."""
        try:
            return self.context["view"].kwargs[self.field_name]
        except:
            serializers.ValidationError("%s not found in kwargs." % self.field_name)

    def to_representation(self, value):
        """
        Override the returning method.

        This function will check if the serializer is supplied
        in case of foreign key field. In case of foreign key, the
        value will be and object. If it is  normal id then it is
        going to be type int.
        """
        if not value:
            return None
        if self.serializer:
            try:
                return self.serializer(value).data
            except:
                print("except")
                pass
        if isinstance(value, int):
            return encode(value)
        try:
            return encode(value.id)
        except:
            return None

    def to_internal_value(self, value):
        """To convert value for saving."""
        return value


class RequestIPField(serializers.Field):
    """Encoded id field."""

    def get_value(self, dictionary):
        """
        Function wil get the user's IP address from the request
        """
        try:
            ip = self.context["view"].request.META.get("REMOTE_ADDR")
            x_forwarded_for = self.context["view"].request.META.get(
                "HTTP_X_FORWARDED_FOR"
            )
            if not ip and x_forwarded_for:
                ip = x_forwarded_for.split(",")[0]
            return ip
        except:
            if self.required:
                raise serializers.ValidationError("IP not found")

    def to_internal_value(self, value):
        """To convert value for saving."""
        return value
