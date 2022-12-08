"""Views related to user account and tokens."""

from rest_framework.views import APIView
from rest_framework import generics


from common.exceptions import BadRequest

from common import library as comm_lib

from v1.accounts import permissions as user_permissions

from v1.accounts.constants import VTokenTypeChoices
from v1.accounts.constants import VTokenStatusChoices

from v1.accounts.models import ProjectUser
from v1.accounts.models import ValidationToken

from v1.accounts.serializers import user as user_serializers
from v1.accounts.serializers import auth as auth_serializers


# accounts/validate/username/
class ValidateUsername(generics.RetrieveAPIView):
    """View to check username availability."""

    serializer_class = auth_serializers.ValidateUsernameSerializer

    @staticmethod
    def post(request, *args, **kwargs):  # TODO: remove post here
        """
        Function to get username availability.

        Request Params:
            username(str): user name.
            type(int): type of user account.
        Response:
            Response. with,
            success(bool): success status of the response.
            message(str): Status description message.
            code(int): status code.
            data(dict): data info.
                valid(bool): true or false value.
                available(bool): true or false value.
                message(str): validation message
        """
        serializer = auth_serializers.ValidateUsernameSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)

        return comm_lib.success_response(serializer.data)


# accounts/validate/password/
class ValidatePassword(generics.RetrieveAPIView):
    """View to check password validity."""

    @staticmethod
    def post(request, *args, **kwargs):  # TODO: remove post
        """
        Function to get username availability.

        Request Params:
            password(str): password.
            type(int): type of user account.
        Response:
            Response. with,
            success(bool): success status of the response.
            message(str): Status description message.
            code(int): status code.
            data(dict): data info.
                valid(bool): true or false value.
                message(str): validation message
        """
        serializer = auth_serializers.ValidatePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            raise BadRequest(serializer.errors)

        return comm_lib.success_response(serializer.data)


# accounts/validator/
class ManageValidator(APIView):
    """View to perform validation token management."""

    # TODO: Move logic to serializer
    http_method_names = ["get", "post"]

    @staticmethod
    def fetch_token_salt(request):
        try:
            key = request.data["token"]
            pk = request.data["salt"]
        except:
            key = request.query_params["token"]
            pk = request.query_params["salt"]
        if not key:
            raise BadRequest("token can not be empty")
        if not pk:
            raise BadRequest("salt can not be empty")
        return key, pk

    @staticmethod
    def check_token_validity(key, pk):
        try:
            token = ValidationToken.objects.get(
                id=comm_lib.decode(pk),
                key=key,
                status=VTokenStatusChoices.VTOKEN_STATUS_UNUSED,
            )

            if not token.is_valid:
                token = None
        except:
            token = None
        return token

    def validate(self, request, token=None):
        """
        Function to execute validation token.

        Request Params:
            Following params are mandatory in the request body,
            salt(char): salt value.
            token(char): 90 digit reset token.

            Following params are supplied from the permissions,
            token(obj): validation token object.
        Response:
            Response:
            Response. with,
            success(bool): success status of the response.
            message(str): Status description message.
            code(int): status code.
            data(dict): data info.
                valid(bool): true or false value.
        """

        key, pk = self.fetch_token_salt(request)
        token = self.check_token_validity(key, pk)
        resp = {}

        if token:
            token.user.email_verified = True
            token.user.save()
            if (
                token.user.password
                and token.type != VTokenTypeChoices.VTOKEN_TYPE_RESET_PASS
            ):
                resp["set_password"] = False
            else:
                resp["set_password"] = True
            if token.type == VTokenTypeChoices.VTOKEN_TYPE_VERIFY_EMAIL:
                token.mark_as_used()
                resp["valid"] = True
                resp["message"] = "Verification completed."
            elif token.type == VTokenTypeChoices.VTOKEN_TYPE_CHANGE_EMAIL:
                token.mark_as_used()
                success = token.user.confirm_updated_email()
                if success:
                    resp["valid"] = True
                    resp["message"] = "Verification completed. Email changed"
            else:
                resp["valid"] = True
                resp["message"] = "Token is valid and active."
        else:
            resp["set_password"] = False
            resp["valid"] = False
            resp["message"] = "Token is invalid/expired."
        return comm_lib.success_response(resp)

    def get(self, request, token=None, *args, **kwargs):
        """GET request end point"""
        return self.validate(request, token)

    def post(self, request, token=None, *args, **kwargs):
        """POST request end point"""
        return self.validate(request, token)


# accounts/shop/signup/
class Signup(generics.CreateAPIView):
    """View to Sign up user."""

    serializer_class = user_serializers.UserSerializer


# accounts/device/
class CreateUserDevice(generics.CreateAPIView):
    """User device create."""

    serializer_class = user_serializers.UserDeviceSerializer
    permission_classes = (user_permissions.IsAuthenticated,)

    def get_serializer_context(self):
        """Overriding method to pass user."""
        self.request.data["user"] = self.kwargs["user"].id
        self.request.data["creator"] = self.kwargs["user"].id
        return {"request": self.request}


# accounts/login
class Login(generics.CreateAPIView):
    """Login view."""

    serializer_class = auth_serializers.LoginSerializer


# accounts/login/magic
class MagicLogin(generics.CreateAPIView):
    """Login with magic link."""

    # TODO: user IsValidationTokenValid permission

    serializer_class = auth_serializers.MagicLoginSerializer


# accounts/logout
class Logout(APIView):
    """View to logout."""

    permission_classes = (user_permissions.IsAuthenticated,)
    http_method_names = [
        "post",
    ]

    def post(
        self, request, user=None, *args, **kwargs
    ):  # TODO: check and move to serializer
        """
        Post method to logout.

        Request Params:
            Body:
                device_id(str): optional device id to delete device.
            kwargs:
                account(obj): user account.
        Response:
            Success response.
        """
        device_id = request.data.get("device_id", None)
        user.logout(device_id)

        return comm_lib.success_response({}, "Logout successful", 200)


class ResetPassword(generics.CreateAPIView):  # TODO: change to send reset password link
    """View to create reset password."""

    def post(self, request, *args, **kwargs):  # TODO: check and move to serializer
        """Post method to send password reset email."""
        try:
            user = ProjectUser.objects.get(email=request.data["email"])
        except:
            raise BadRequest("Invalid email, reset failed.")
        success = user.reset_password()
        if not success:
            raise BadRequest("Invalid email, reset failed.")

        return comm_lib.success_response({}, "Reset initiated.", 200)


class SetPassword(generics.CreateAPIView):
    """View to set password after forgot password"""

    permission_classes = (user_permissions.IsValidationTokenValid,)

    def post(self, request, *args, **kwargs):  # TODO: move to serializer
        """Post method to set user password"""
        password = request.data.get("password", None)
        if not password:
            raise BadRequest("Password not found")
        valid, message = comm_lib.validate_password(password)
        if not valid:
            raise BadRequest(message)
        kwargs["token"].user.set_password(password)
        kwargs["token"].user.save()
        kwargs["token"].mark_as_used()
        login = auth_serializers.LoginSerializer(kwargs["token"].user)

        return comm_lib.success_response(
            login.data, "Password reset successful. Please login", 200
        )


# accounts/magic/generate/
class MagicLink(generics.CreateAPIView):
    """View to generate magic link"""

    serializer_class = auth_serializers.MagicLinkSerializer


class VerificationEmail(generics.CreateAPIView):
    """View to verify the usr email"""

    permission_classes = (user_permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """Post method to resend verification email"""
        request.user.verify_email()

        return comm_lib.success_response({}, "Email sent successfully.", 200)
