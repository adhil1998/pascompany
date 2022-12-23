from rest_framework import permissions
from common.exceptions import BadRequest, UnauthorizedAccess
from common.functions import decode
from accounts.models import AccessToken, User


class IsAuthenticated(permissions.BasePermission):
    """
    Check if the user is authenticated.
    """

    def has_permission(self, request, view):
        """Function to check token."""
        key = request.META.get('HTTP_BEARER')
        user_id = decode(request.META.get('HTTP_USER_ID'))
        if not key:
            raise BadRequest(
                'Can not find Bearer token in the request header.')
        if not user_id:
            raise BadRequest('Can not find User-Id in the request header.')
        try:
            user = AccessToken.objects.get(key=key, user__id=user_id).user
        except:
            raise UnauthorizedAccess(
                'Invalid Bearer token or User-Id, please re-login.')
        request.user = user
        view.kwargs['user'] = user
        return True
