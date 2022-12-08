"""Views related to user account and tokens."""

from sentry_sdk import capture_exception

from rest_framework.views import APIView
from rest_framework import generics

from common.exceptions import BadRequest
from common.views import MultiPermissionView

from v1.accounts import permissions as user_permissions

from v1.accounts.models import ProjectUser
from v1.accounts.models import TermsAndConditions

from v1.accounts.filters import UserFilter

from v1.accounts.serializers import user as user_serializers


# accounts/user/<id:optional>/
class UserDetails(
    generics.RetrieveUpdateAPIView, 
    generics.ListAPIView, 
    MultiPermissionView
):
    """View to update user details"""

    # TODO: user details fetch without id
    http_method_names = ["get", "patch"]

    permissions = {
        "GET": (user_permissions.IsAuthenticated,),
        "PATCH": (user_permissions.IsAuthenticated, 
                  user_permissions.HasUserAccess
                  ),
    }

    serializer_class = user_serializers.UserSerializer
    queryset = ProjectUser.objects.all()


class UserList(generics.ListAPIView):
    """List users"""

    # TODO: change url
    permission_classes = (user_permissions.IsAuthenticated,)
    serializer_class = (
        user_serializers.UserListSerializer
    )  # TODO: use user serializer with min_mode

    filterset_class = UserFilter
    queryset = ProjectUser.objects.all()


class TermsAndConditionsDetails(generics.RetrieveAPIView):
    """
    API to get latest terms and conditions
    """

    permission_classes = (user_permissions.ValidTOTP,)

    serializer_class = user_serializers.TermsAndConditionsSerializer

    def get_object(self):
        try:
            return TermsAndConditions.objects.get(default=True)
        except TermsAndConditions.MultipleObjectsReturned as e:
            capture_exception(e)
            return TermsAndConditions.objects.filter(default=True).last()
        except TermsAndConditions.DoesNotExist as e:
            capture_exception(e)
            raise BadRequest("Terms and Conditions not added")
