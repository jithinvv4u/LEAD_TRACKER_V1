""" Comming Base Views"""

from rest_framework.views import APIView
from common.exceptions import BadRequest


class MultiPermissionView(APIView):
    """
    Permissions can be defined using permissions attribute with a dictionary
    with the type of request as key and permission as value
    """

    permissions = {}

    def get_permissions(self):
        try:
            self.permission_classes = self.permissions[self.request.method]
        except KeyError:
            raise BadRequest("Method not allowed")
        return super(MultiPermissionView, self).get_permissions()
