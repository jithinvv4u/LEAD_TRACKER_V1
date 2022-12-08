"""Permissions of the app accounts."""

import pyotp

from django.conf import settings
from rest_framework import permissions

from common.exceptions import BadRequest
from common.exceptions import UnauthorizedAccess
from common.exceptions import AccessForbidden

from common.library import decode

from .models import AccessToken
from .models import ValidationToken


class IsAuthenticated(permissions.BasePermission):
    """
    Check if the user is authenticated.

    Authentication to check if the user access token is valid
    and fetch the user from the token and add it to kwargs.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get("HTTP_AUTHORIZATION")
        user_id = decode(request.META.get("HTTP_USER_ID"))
        if not key:
            raise BadRequest("Can not find Bearer token in the request header.")
        if not user_id:
            raise BadRequest("Can not find User-Id in the request header.")

        try:
            user = AccessToken.objects.get(key=key, user__id=user_id).user
        except:
            raise UnauthorizedAccess(
                "Invalid Bearer token or User-Id, please re-login."
            )

        if user.blocked:
            raise AccessForbidden("user account is blocked, contact admin.")

        request.user = user
        view.kwargs["user"] = user

        return True


class IsAuthenticatedWithVerifiedEmail(permissions.BasePermission):
    """
    Check if the user had verified email.

    Authentication to check if the user has verified his email.
    Access to certain parts of the app will be limited if the user has not
    verified his email.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get("HTTP_BEARER")
        user_id = decode(request.META.get("HTTP_USER_ID"))
        if not key:
            raise BadRequest("Can not find Bearer token in the request header.")
        if not user_id:
            raise BadRequest("Can not find User-Id in the request header.")

        try:
            user = AccessToken.objects.get(key=key, user__id=user_id).user
        except:
            raise UnauthorizedAccess(
                "Invalid Bearer token or User-Id, please re-login."
            )

        if user.blocked:
            raise AccessForbidden("User account is blocked, contact admin.")

        if not user.email_verified:
            raise AccessForbidden("User has not verified email.")
        request.user = user
        view.kwargs["user"] = user
        return True


class IsValidationTokenValid(permissions.BasePermission):
    """
    Permission to check if the validation token is valid.

    This class will fetch the validation token from the request
    params and add it into kwargs if the token is valid else add
    None.
    """

    def has_permission(self, request, view):
        """Function to check validation token."""
        key = request.META.get("HTTP_TOKEN")
        pk = decode(request.META.get("HTTP_SALT"))
        if not key:
            raise BadRequest("Token not found in Header")
        if not pk:
            raise BadRequest("Salt not found in Header")

        try:
            token = ValidationToken.objects.get(id=decode(pk), key=key)
            if not token.is_valid:
                raise UnauthorizedAccess("Invalid token.")

        except:
            raise UnauthorizedAccess("Invalid token.")
        view.kwargs["token"] = token
        return True


class HasUserAccess(permissions.BasePermission):
    """
    This can only be called along with and after IsAuthenticated

    Checks if signed-in user has access to edit the query user.
    If both of them is the same, true is returned
    """

    def has_permission(self, request, view):
        """Function to check token."""
        query_user_id = view.kwargs.get("pk", None)
        if not query_user_id or query_user_id == request.user.id:
            view.kwargs["pk"] = request.user.id
            return True
        raise AccessForbidden("Access denied.")


class ValidTOTP(permissions.BasePermission):
    """
    Check if a valid TOTP is passed in the headed for unauthenticated requests
    """

    def has_permission(self, request, view):
        """Function to check totp."""
        if settings.ENVIRONMENT == "local":
            return True
        current_otp = request.META.get("HTTP_OTP")
        if not current_otp:
            raise BadRequest("Can not find OTP in the request header.")
        totp = pyotp.TOTP(settings.TOTP_TOKEN)
        if totp.verify(current_otp, valid_window=1):
            return True
        raise UnauthorizedAccess("Invalid OTP.", send_to_sentry=False)
