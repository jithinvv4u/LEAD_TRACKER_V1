"""Models of the app Accounts."""
from __future__ import unicode_literals

from datetime import timedelta

from fcm_django.models import AbstractFCMDevice

from django.db import models
from django.contrib.auth.models import AbstractUser as DjangoAbstractUser
from django.utils import timezone
from django.utils.crypto import get_random_string

from django.conf import settings

from common.library import anonymise_email
from common.library import date_time_desc
from common.library import generate_random_number
from common.library import encode
from common.library import get_file_path

from common.models import AbstractBaseModel

from common import vendors

from v1.communications.models import Notification

from .notification_data import get_notification_data

from .constants import UserTypeChoices
from .constants import LanguageChoices
from .constants import VTokenTypeChoices
from .constants import VTokenStatusChoices
from .constants import DeviceTypeChoices
from .constants import UserStatusChoices

from .constants import TOKEN_VALIDITY
from .constants import MESSAGE_USER_OTP


class AbstractPerson(models.Model):
    """
    Abstract Model to store common details of a person
    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, default="", blank=True, null=True)
    gender = models.CharField(max_length=50, default="", blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    birth_city = models.CharField(max_length=500, default="", blank=True, null=True)
    marital_status = models.CharField(max_length=50, default="", blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, default="", blank=True, null=True)

    def get_or_create_user(self):
        """Django user for the corresponding person object"""
        try:
            user = ProjectUser.objects.get(email=self.email)
            created = False
        except:
            user = ProjectUser.objects.create(email=self.email, username=self.email)
            created = True
        if created:
            user.first_name = self.first_name.title()
            user.last_name = self.last_name.title()
            user.dob = self.dob
            user.phone = self.phone
            user.save()
        return user

    class Meta:
        """Meta class for the above model."""

        abstract = True


class Person(AbstractPerson):
    """
    Non Abstract model for Person
    """

    def __str__(self):
        return "%s %s - %d" % (self.first_name, self.last_name, self.id)


class ProjectUser(DjangoAbstractUser):
    """
    ProjectUser model.

    Attribs:
        user (obj): Django user model.
        blocked(bool): field which shows the active status of user.
        terms_accepted(bool): boolean value indicating whether the
            terms are accepted by the user.
        address(str): address of the user.
        phone (str): phone number of the user
        type (int): field define the type of the user like
            admin or Normal user etc.
        language(int): Language preference.
        image (img): user image.
        dob(datetime): date of birth of user.
    """

    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(default="", max_length=200, blank=True)
    address = models.CharField(default="", max_length=2000, blank=True)
    language = models.IntegerField(
        default=LanguageChoices.LANGUAGE_ENG, choices=LanguageChoices.choices()
    )
    image = models.ImageField(
        upload_to=get_file_path, null=True, default=None, blank=True
    )
    type = models.IntegerField(
        default=UserTypeChoices.USER_TYPE_ADMIN, choices=UserTypeChoices.choices()
    )
    status = models.IntegerField(
        default=UserStatusChoices.USER_STATUS_CREATED,
        choices=UserStatusChoices.choices(),
    )

    terms_accepted = models.BooleanField(default=False)
    privacy_accepted = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    blocked = models.BooleanField(default=False)
    # updated_email = models.EmailField(null=True, blank=True, default="")

    def __str__(self):
        """Object name in django admin."""
        return "%s : %s" % (self.name, self.id)

    @property
    def image_url(self):
        """Get file url ."""
        try:
            return self.image.url
        except:
            return None

    @property
    def name(self):
        """Get user full name."""
        return "%s" % (self.get_full_name())

    @property
    def idencode(self):
        """To return encoded id."""
        return encode(self.id)

    @property
    def anony_email(self):
        """Property to get anonymous email."""
        return anonymise_email(self.email)

    @property
    def anony_updated_email(self):
        """Property to get anonymous email."""
        return anonymise_email(self.updated_email)

    def devices(self):
        """Function to get user devices."""
        return UserDevice.objects.filter(user=self, active=True)

    def issue_access_token(self):
        """Function to get or create user access token."""
        token, created = AccessToken.objects.get_or_create(user=self)
        self.last_login = timezone.now()
        self.save()
        # if not created:
        #     token.refresh()
        return token.key

    def logout(self, device_id=None):
        """Function for user to logout."""
        try:
            token = AccessToken.objects.get(user=self)
            token.refresh()
        except:
            pass
        if device_id:
            devices = UserDevice.objects.filter(user=self, device_id=device_id)
            for device in devices:
                device.active = False
                device.updater = self
                device.save()
        return True

    # def set_password(self):
    #     """Function to set password."""
    #     if self.type == USER_TYPE_ADMIN:
    #         return (ValidationToken.initialize(self, VTokenTypeChoices.VTOKEN_TYPE_SET_PASS))

    def reset_password(self):
        """Function to set password."""
        return ValidationToken.initialize(
            self, VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS
        )

    def verify_email(self):
        """Function to send email verification"""
        return ValidationToken.initialize(
            self, VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL
        )

    def verify_new_email(self):
        """Function to send email verification"""
        return ValidationToken.initialize(
            self, VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL
        )

    def generate_magic_link(self):
        """Function to send email verification"""
        return ValidationToken.initialize(self, VTokenTypeChoices.VTOKEN_TYPE_MAGIC)

    def confirm_updated_email(self):
        """
        Function to update the email of the user.
        Updates email and username to updated_email and sets
        updated email as blank
        """
        if self.updated_email:
            self.email = self.updated_email
            self.username = self.updated_email
            self.updated_email = ""
            self.save()
            return True
        return False


class ValidationToken(AbstractBaseModel):
    """
    Class to store the validation token data.

    This is a generic model to store and validate all
    sort of tokens including password setters, one time
    passwords and email validations
    Attribs:
        user(obj): user object
        req_browser(str): browser of the user requested.
        req_location(str): location of the request created.
        set_browser(str): browser of the user updated.
        set_location(str): location of the request updated.
        key (str): token.
        status(int): status of the validation token
        expiry(datetime): time up to which link is valid.
        type(int): type indicating the event associated.
    """

    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    add_info = models.JSONField(
        default=dict, null=True, blank=True, verbose_name="additional_info"
    )

    key = models.CharField(default="", max_length=200, blank=True)
    status = models.IntegerField(
        default=VTokenStatusChoices.VTOKEN_STATUS_UNUSED,
        choices=VTokenStatusChoices.choices(),
    )
    expiry = models.DateTimeField(default=timezone.now)
    type = models.IntegerField(default=0, choices=VTokenTypeChoices.choices())

    def __str__(self):
        """Object name in django admin."""
        return str(self.user.name) + ": " + str(self.key) + ":  " + str(self.id)

    def save(self, *args, **kwargs):
        """
        Overriding the default save signal.

        This function will generate the token key based on the
        type of the token and save when the save() function
        is called if the key is empty. It. will. also set the
        expiry when the object is created for the first time.
        """
        if not self.key:
            self.key = self.generate_unique_key()
        if not self.id:
            self.expiry = self.get_expiry()
        return super(ValidationToken, self).save(*args, **kwargs)

    def get_validity_period(self):
        return TOKEN_VALIDITY[self.type]

    def get_expiry(self):
        """Function to get the validity based on type."""
        validity = self.get_validity_period()
        return timezone.now() + timedelta(minutes=validity)

    def generate_unique_key(self):
        """Function to generate unique key."""
        if self.type != VTokenTypeChoices.VTOKEN_TYPE_OTP:
            key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        else:
            key = generate_random_number(settings.OTP_LENGTH)

        if ValidationToken.objects.filter(
            key=key, type=self.type, status=VTokenStatusChoices.VTOKEN_STATUS_UNUSED
        ).exists():
            key = self.generate_unique_key()
        return key

    def validate(self):
        """Function to. validate the token."""
        status = True
        if not self.is_valid:
            status = False
        self.status = VTokenStatusChoices.VTOKEN_STATUS_USED
        self.updater = self.user
        self.save()
        return status

    def send_otp(self):
        """Function to send OTP to citizen."""
        if self.is_valid and self.type == VTokenTypeChoices.VTOKEN_TYPE_OTP:
            mobile = self.user.username
            message = MESSAGE_USER_OTP % (self.key, self.get_validity_period())
            vendors.send_sms(mobile, message)
        return True

    def notify(self):
        """Function to create notification."""
        if not self.is_valid:
            return False
        if self.type == VTokenTypeChoices.VTOKEN_TYPE_OTP:
            self.send_otp()
        notif_params = get_notification_data(self)
        Notification.notify(**notif_params)
        return True

    def refresh(self):
        """Function  to refresh the validation token."""
        if not self.is_valid:
            self.key = self.generate_unique_key()
            self.status = VTokenStatusChoices.VTOKEN_STATUS_UNUSED
        self.expiry = self.get_expiry()
        self.updater = self.user
        self.save()
        return True

    def mark_as_used(self):
        """Function to mark validation token as used"""
        self.status = VTokenStatusChoices.VTOKEN_STATUS_USED
        self.save()

    @staticmethod
    def initialize(user, type):
        """Function to initialize verification."""
        validation, created = ValidationToken.objects.get_or_create(
            user=user,
            status=VTokenStatusChoices.VTOKEN_STATUS_UNUSED,
            type=type,
            creator=user,
        )
        if not created:
            validation.refresh()
        return validation.notify()

    @property
    def validity(self):
        """Function to get the validity of token."""
        return date_time_desc(self.expiry)

    @property
    def created_on_desc(self):
        """Function to get the validity of token."""
        return date_time_desc(self.created_on)

    @property
    def is_valid(self):
        """Function  which check if Validator is valid."""
        if self.expiry > timezone.now() and (
            self.status == VTokenStatusChoices.VTOKEN_STATUS_UNUSED
        ):
            return True
        return False


class AccessToken(models.Model):
    """
    The default authorization token model.

    This model is overriding the DRF token
    Attribs:
        user(obj): user object
        Key(str): token
        created(datetime): created date and time.
    """

    user = models.ForeignKey(
        ProjectUser, related_name="auth_token", on_delete=models.CASCADE
    )
    key = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Function to return value in django admin."""
        return self.key

    def save(self, *args, **kwargs):
        """Overriding the save method to generate key."""
        if not self.key:
            self.key = self.generate_unique_key()
        return super(AccessToken, self).save(*args, **kwargs)

    def generate_unique_key(self):
        """Function to generate unique key."""
        key = get_random_string(settings.ACCESS_TOKEN_LENGTH)
        if AccessToken.objects.filter(key=key).exists():
            self.generate_unique_key()
        return key

    def refresh(self):
        """Function  to change token."""
        self.key = self.generate_unique_key()
        self.save()


class UserDevice(AbstractFCMDevice, AbstractBaseModel):
    """
    Class for user devices.

    This is inherited from the AbstractFCMDevice and
    AbstractBaseModel.

    Attribs:
        user(obj): user object.
        type(int): device types
    Attribs Inherited:
        name(str): name of the device
        active(bool): bool value.
        date_created(datetime): created time.
        device_id(str): Device id
        registration_id(str): Reg id
    """

    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    type = models.IntegerField(
        default=DeviceTypeChoices.DEVICE_TYPE_ANDROID,
        choices=DeviceTypeChoices.choices(),
    )
    registration_id = models.TextField(
        verbose_name=("Registration token"), blank=True, default=""
    )

    class Meta:
        """Meta data."""

        verbose_name = "User device"
        verbose_name_plural = "User devices"


class TermsAndConditions(AbstractBaseModel):
    """
    Model to store different versions of terms and conditions
    Attributes:
        title(str)      : Title of Terms & Conditions
        version(int)    : Version of Terms & Conditions
    """

    title = models.CharField(max_length=100, null=True, blank=True)
    version = models.CharField(max_length=20)
    default = models.BooleanField(default=False)

    def __str__(self):
        return f"V{self.version} - {self.title})"

    def make_default(self):
        for tc in TermsAndConditions.objects.all():
            tc.default = False
            tc.save()
        self.default = True
        self.save()


class UserTCAcceptance(AbstractBaseModel):
    """
    Model to store details and proof of user's acceptance of terms and conditions
    Attributes:
        user(obj)   : User who accepted the T&C
        tc(obj)     : Terms & conditions that the user accepted
        ip(str)     : IP Address from which the user accepted the terms
    """

    user = models.ForeignKey(ProjectUser, on_delete=models.CASCADE)
    tc = models.ForeignKey(TermsAndConditions, on_delete=models.CASCADE)
    ip = models.CharField(max_length=50, null=True, blank=True)
