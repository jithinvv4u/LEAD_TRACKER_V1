"""Constants used in the app Accounts."""

from v1.communications import constants as comm_constants
from common.library import ChoiceAdapter


# User types
class UserTypeChoices(ChoiceAdapter):
    USER_TYPE_ADMIN = 1


# User language
class LanguageChoices(ChoiceAdapter):
    LANGUAGE_ENG = 1


# Validation token type
class VTokenTypeChoices(ChoiceAdapter):
    VTOKEN_TYPE_SET_PASS = 1
    VTOKEN_TYPE_RESET_PASS = 2
    VTOKEN_TYPE_VERIFY_EMAIL = 3
    VTOKEN_TYPE_OTP = 4
    VTOKEN_TYPE_MAGIC = 5
    VTOKEN_TYPE_CHANGE_EMAIL = 6


# Validation token status
class VTokenStatusChoices(ChoiceAdapter):
    VTOKEN_STATUS_UNUSED = 1
    VTOKEN_STATUS_USED = 2


# Device types
class DeviceTypeChoices(ChoiceAdapter):
    DEVICE_TYPE_ANDROID = 1
    DEVICE_TYPE_IOS = 2
    DEVICE_TYPE_WEB = 3


# User Status choices
class UserStatusChoices(ChoiceAdapter):
    USER_STATUS_CREATED = 1


# Validity in Minutes
_30_MINUTES = 30  # 30 Minutes
_1_DAY = 1440  # 24 hours
_2_DAY = 2880  # 24 hours
_365_DAYS = 525600  # 365 days

TOKEN_VALIDITY = {
    VTokenTypeChoices.VTOKEN_TYPE_SET_PASS: _1_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS: _2_DAY,
    VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL: _365_DAYS,
    VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL: _365_DAYS,
    VTokenTypeChoices.VTOKEN_TYPE_OTP: _30_MINUTES,
    VTokenTypeChoices.VTOKEN_TYPE_MAGIC: _2_DAY,
}

# Messages

MESSAGE_USER_OTP = "%s is your OTP for leadtracker_v1 and it will expire in %s minutes."
MESSAGE_OTP_INVALID = "Invalid OTP."
MESSAGE_OTP_EXPIRED = "OTP is expired/used. Please re-initiate."
MESSAGE_OTP_VALIDATED = "OTP Validated Successfully"
