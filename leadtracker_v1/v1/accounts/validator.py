"""Module for accounts field custom Validator."""

from common.exceptions import BadRequest

from common.library import validate_email
from common.library import validate_phone

from v1.accounts.models import ProjectUser


def validate_username(username):
    """
    Function to validate username.

    Input Params:
        username(str): username to check
        user_type(int): user type.
    Return:
        data(dict): data dictionary with,
            valid(bool): true if valid
            available(bool): true if available.
            message(str): message
    """
    response = {"available": False, "valid": False}

    valid, message = validate_email(username)
    if not valid:
        response["message"] = message
        return response
    response["valid"] = True
    if ProjectUser.objects.filter(username=username).exists():
        response["message"] = "Username is already taken."
        return response
    response["message"] = "Username is available."
    response["available"] = True
    return response
