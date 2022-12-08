"""
Models of the app Communication.

All models related to the Communications and notifications are managed
in this app.
"""
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

from common import vendors
from common.models import AbstractBaseModel

from .content_manager import get_content
from .content_manager import get_email_template
from .content_manager import get_from_email

from .constants import NotificationActionChoices
from .constants import NotificationTypeChoices
from .constants import ObjectTypeChoices


class Notification(AbstractBaseModel):
    """
    Class for managing user notification.

    Attribs:
        user(obj): User object
        devices(objs): device to which notification initiated.
        is_read(bool): to mark if the notification is
            read by the user.
        title_en(str): notification message title in English.
        body_en(str): notification message body in English
        title_loc(str): notification message title in local language.
        body_loc(str): notification message body in local language
        action(int): notification type based on which
            sending emails or push notification is decided.
        event(int): notification event
        event_id(int): event id.
        type(int): notification type for identifying the notification
            when it is pushed to devices.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    devices = models.ManyToManyField("accounts.UserDevice", blank=True)
    is_read = models.BooleanField(default=False)
    visibility = models.BooleanField(default=True)
    title_en = models.CharField(default="", max_length=300)
    title_loc = models.CharField(default="", max_length=300, blank=True)
    body_en = models.CharField(default="", max_length=500)
    body_loc = models.CharField(default="", max_length=500, blank=True)
    action_url = models.CharField(default="", max_length=500, blank=True)
    action = models.IntegerField(
        default=NotificationActionChoices.NOTIF_ACTION_NORMAL,
        choices=NotificationActionChoices.choices(),
    )
    event = models.IntegerField(default=0, choices=ObjectTypeChoices.choices())
    event_id = models.CharField(default="", max_length=50)
    type = models.IntegerField(default=0, choices=NotificationTypeChoices.choices())
    context = models.JSONField(null=True, blank=True)
    send_to = models.EmailField(null=True, blank=True, default="")

    class Meta:
        """Meta class for the above model."""

        ordering = ("-created_on",)

    def __str__(self):
        """Function to return value in django admin."""
        return "%s-%s: %s" % (self.user.name, self.title_en, self.idencode)

    @staticmethod
    def notify(token, event, user, notif_type, resend=False, send_to="", context=None):
        """Function to create notification of an event."""
        content = get_content(notif_type)
        context = {} if not context else context

        notification, created = Notification.objects.get_or_create(
            user=user,
            action=content["action"],
            event=content["event"],
            event_id=event.idencode,
            type=notif_type,
            send_to=send_to,
        )
        if created:
            notification.creator = event.creator
        else:
            notification.updater = event.creator
        notification.title_en = content["title_en"].format(**vars())
        notification.title_loc = content["title_loc"].format(**vars())
        notification.body_en = content["body_en"].format(**vars())
        notification.body_loc = content["body_loc"].format(**vars())
        notification.action_url = content["action_url"].format(**vars())
        notification.visibility = content["visibility"]
        notification.context = context
        notification.save()
        for device in user.devices():
            notification.devices.add(device)
        if created or resend:
            notification.send(event)

    def send(self, event):
        """Send notification."""
        if self.action == NotificationActionChoices.NOTIF_ACTION_EMAIL:
            vendors.send_notification_email(self, event)
        elif self.action == NotificationActionChoices.NOTIF_ACTION_PUSH:
            vendors.send_push_notification(self)
        elif self.action == NotificationActionChoices.NOTIF_ACTION_PUSH_N_EMAIL:
            vendors.send_push_notification(self)
            vendors.send_notification_email(self, event)
        elif self.action == NotificationActionChoices.NOTIF_ACTION_PUSH_EMAIL_N_SMS:
            vendors.send_push_notification(self)
            vendors.send_sms(self.user.phone, self.body_en)
            vendors.send_notification_email(self, event)
        elif self.action == NotificationActionChoices.NOTIF_ACTION_EMAIL_N_SMS:
            vendors.send_sms(self.user.phone, self.body_en)
            vendors.send_notification_email(self, event)

    def email_template(self):
        """Function to get email template."""
        path = get_email_template(self)
        if path:
            return settings.TEMPLATES_DIR + path
        return ""

    def from_email(self):
        """Function to get email template."""
        return get_from_email(self)

    def read(self):
        """Function to read notification."""
        self.is_read = True
        self.save()

    @property
    def to_email(self):
        """
        Return to email.
        Defaults to user's email if send_to is not specified.
        Created to managed email verification for email changes.
        """
        if self.send_to:
            return self.send_to
        return self.user.email
