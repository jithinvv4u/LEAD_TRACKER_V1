"""
Module to manage notification content.

This module act as a content creator for notifications.
The content and emails template of each type of user for
each notification types are defined in the content
dictionary. content is generated based on the user type
and notification type.

Only object of the corresponding event is allowed as
context variables in messages.
"""

from django.conf import settings

from . import constants as notif_constants


content = {
    notif_constants.NotificationTypeChoices.NOTIF_TYPE_VERIFY_EMAIL: {
        "title_en": "Verify your Fairfood email.",
        "title_loc": "Verify your Fairfood email.",
        "body_en": "Verify your email {event.user.anony_email} "
        + "linked with Fairfood Account.",
        "body_loc": "Verify your email {event.user.anony_email} "
        + "linked with Fairfood Account.",
        "visibility": False,
        "action": notif_constants.NotificationActionChoices.NOTIF_ACTION_EMAIL,
        "email": "/emails/account/verify_email.html",
        "event": notif_constants.ObjectTypeChoices.OBJECT_TYPE_USER,
        "from_email": "Trace <trace@fairfood.org>",
        "action_url": settings.FRONT_ROOT_URL
        + "/verify/?token={event.key}&salt={event.idencode}&notification={notification.idencode}"
        "&user={user.idencode}",
    },
    notif_constants.NotificationTypeChoices.NOTIF_TYPE_CHANGE_EMAIL: {
        "title_en": "Verify your new email.",
        "title_loc": "Verify your new email.",
        "body_en": "Verify your email {event.user.anony_updated_email} "
        + "The email will be changed only when you verify the new email.",
        "body_loc": "Verify your email {event.user.anony_updated_email} "
        + "The email will be changed only when you verify the new email.",
        "visibility": True,
        "action": notif_constants.NotificationActionChoices.NOTIF_ACTION_EMAIL,
        "email": "/emails/account/verify_new_email.html",
        "event": notif_constants.ObjectTypeChoices.OBJECT_TYPE_USER,
        "from_email": "Trace <trace@fairfood.org>",
        "action_url": settings.FRONT_ROOT_URL
        + "/verify/?token={event.key}&salt={event.idencode}&notification={notification.idencode}"
        "&user={user.idencode}",
    },
    notif_constants.NotificationTypeChoices.NOTIF_TYPE_RESET_PASSWORD: {
        "title_en": "Reset your Fairfood account password.",
        "title_loc": "Reset your Fairfood account password.",
        "body_en": "",
        "body_loc": "",
        "visibility": False,
        "action": notif_constants.NotificationActionChoices.NOTIF_ACTION_EMAIL,
        "email": "/emails/account/reset_password.html",
        "event": notif_constants.ObjectTypeChoices.OBJECT_TYPE_USER,
        "from_email": "Trace <trace@fairfood.org>",
        "action_url": settings.FRONT_ROOT_URL
        + "/reset/?token={event.key}&salt={event.idencode}&notification={notification.idencode}"
        "&user={user.idencode}",
    },
    notif_constants.NotificationTypeChoices.NOTIF_TYPE_MAGIC_LOGIN: {
        "title_en": "Login to your Fairfood account.",
        "title_loc": "Login to your Fairfood account.",
        "body_en": "",
        "body_loc": "",
        "visibility": False,
        "action": notif_constants.NotificationActionChoices.NOTIF_ACTION_EMAIL,
        "email": "/emails/account/magic_login.html",
        "event": notif_constants.ObjectTypeChoices.OBJECT_TYPE_USER,
        "from_email": "Trace <trace@fairfood.org>",
        "action_url": settings.FRONT_ROOT_URL
        + "/login/?token={event.key}&salt={event.idencode}&notification={notification.idencode}"
        "&user={user.idencode}",
    },
}


def get_content(notif_type):
    """
    Function to get notification content.

    Input params:
        notif_type(int): notification type.
        user_type(int): user type.
    Returns:
        Dictionary with,
        title_en(str): notification title in English.
        title_loc(str): notification title in local language.
        body_en(str): notification body in English.
        body_loc(str): notification body in local language.
        action(int): notification action.
    """
    try:
        data = content[notif_type]
        data["title_en"] = data["title_en"].capitalize()
        data["title_loc"] = data["title_loc"].capitalize()
    except:
        data = {
            "title_en": "",
            "title_loc": "",
            "body_en": "",
            "body_loc": "",
            "visibility": True,
            "action": notif_constants.NotificationActionChoices.NOTIF_ACTION_NORMAL,
            "event": 0,
            "action_url": "",
        }
    return data


def get_email_template(notification):
    """Function to get email template."""
    try:
        email = content[notification.type]["email"]
        return email
    except:
        return ""


def get_from_email(notification):
    """Function to get from email address."""
    try:
        from_email = content[notification.type]["from_email"]
        return from_email
    except:
        return ""
