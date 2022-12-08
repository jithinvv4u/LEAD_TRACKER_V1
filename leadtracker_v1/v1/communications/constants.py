"""Constants used in the app communications."""

from common.library import ChoiceAdapter


# Notification Actions
class NotificationActionChoices(ChoiceAdapter):
    NOTIF_ACTION_NORMAL = 1
    NOTIF_ACTION_EMAIL = 2
    NOTIF_ACTION_PUSH = 3
    NOTIF_ACTION_PUSH_N_EMAIL = 4
    NOTIF_ACTION_PUSH_EMAIL_N_SMS = 5
    NOTIF_ACTION_EMAIL_N_SMS = 6


# Notification Type
class NotificationTypeChoices(ChoiceAdapter):
    NOTIF_TYPE_VERIFY_EMAIL = 1
    NOTIF_TYPE_RESET_PASSWORD = 2
    NOTIF_TYPE_MAGIC_LOGIN = 3
    NOTIF_TYPE_CHANGE_EMAIL = 4


# Object types
class ObjectTypeChoices(ChoiceAdapter):
    OBJECT_TYPE_USER = 1
    OBJECT_TYPE_VALIDATION_TOKEN = 2
