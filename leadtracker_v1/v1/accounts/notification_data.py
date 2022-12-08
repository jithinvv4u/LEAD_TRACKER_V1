"""
Get notification data of corresponding event
"""
from v1.accounts.constants import VTokenTypeChoices

from v1.communications.constants import NotificationTypeChoices

NOTIFY_TYPES = {
    VTokenTypeChoices.VTOKEN_TYPE_OTP: 0,
    VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL: NotificationTypeChoices.NOTIF_TYPE_VERIFY_EMAIL,
    VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL: NotificationTypeChoices.NOTIF_TYPE_CHANGE_EMAIL,
    VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS: NotificationTypeChoices.NOTIF_TYPE_RESET_PASSWORD,
    VTokenTypeChoices.VTOKEN_TYPE_MAGIC: NotificationTypeChoices.NOTIF_TYPE_MAGIC_LOGIN,
}


def get_notification_data(object):
    """
    Get notification data from notification object
    Args:
        object: Notification object

    Returns:
        data: Notification data

    """
    notif_params = {
        "token": object,
        "event": object,
        "user": object.user,
        "notif_type": NOTIFY_TYPES[object.type],
        "resend": True,
        "send_to": "",
    }
    if object.type == VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL:
        notif_params["send_to"] = object.user.updated_email
    return notif_params
