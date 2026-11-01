from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_simplejwt.tokens import AccessToken

class HasRole(BasePermission):

    allowed_roles = []

    def has_permission(self, request: Request, view):
        data = request.auth
        # data = AccessToken()

        if not request.user or not request.user.is_authenticated:
            return False

        return data.get("role") in self.allowed_roles