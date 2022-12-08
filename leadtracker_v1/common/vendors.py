"""Commonly used third party libraries and functions."""

from celery.decorators import task
import plivo
from sentry_sdk import capture_exception

from django.conf import settings

from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail


def send_sms(mobile, message):
    """Function to send SMS."""
    try:
        # client = plivo.RestClient(
        #     settings.PLIVO_ID, settings.PLIVO_TOKEN)
        # response = client.messages.create(
        #     src='+31611111111',
        #     dst=mobile,
        #     text=message,
        # )
        # print(response)
        # prints only the message_uuid
        # print(response.message_uuid)
        print("sending sms", message)
        pass

        return True
    except Exception as e:
        capture_exception(e)
        return False


def send_validation_email(validator):
    """Function to create Validator email."""
    html = render_to_string(validator.email_template(), {"validator": validator})
    try:
        send_email.delay(
            validator.email_subject(),
            strip_tags(html),
            validator.email_from(),
            [validator.user.email],
            html,
        )
        print("Email sending success.")
    except Exception as e:
        capture_exception(e)

        print("Email sending failed.")
        pass
    return True


def send_notification_email(notification, event):
    """Function to create Validator email."""
    try:
        notification.action_url = notification.action_url.format(**vars())
    except:
        pass
    html = render_to_string(
        notification.email_template(), {"event": event, "notification": notification}
    )
    to_email = notification.to_email
    if not to_email:
        print("No email address.")
        return False
    try:
        send_email.delay(
            notification.title_en,
            strip_tags(html),
            notification.from_email(),
            [to_email],
            html,
        )
        print("Email sending success.")
    except Exception as e:
        capture_exception(e)
        print("Email sending failed.")
        pass
    return True


def send_push_notification(notification):
    """Function to send push notification."""
    for device in notification.devices.all():
        return None
        # try:
        #     device.send_message(
        #         title=notification.title_en,
        #         body=notification.body_en,
        #         # click_action=push_dict['click_action'],
        #         click_action='FCM_PLUGIN_ACTIVITY',
        #         sound='default',
        #         icon='',
        #         data={
        #             'type': notification.type,
        #             'title': notification.title_en,
        #             'body': notification.body_en
        #         })
        # except Exception as e:
        #     capture_exception(e)
        #     message = 'Failed to send push %s to device %s' % (
        #         notification.id, device.id)
        #     capture_message(message)
        #     pass


@task(name="send_email")
def send_email(subject, text, email_from, to_emails, html):
    """
    Function to send emails.

    Input Params:
        mail_dict(dict): collection dictionary with following details,
            to(list): list of to email ids.
            subject(str): email subject.
            text(str): text content
            html(str): html file
            from: from address
    Return:
        success response
    """
    try:
        send_mail(
            subject, text, email_from, to_emails, fail_silently=False, html_message=html
        )
    except Exception as e:
        capture_exception(e)
