from rest_framework.exceptions import APIException


class BaseAPIException(APIException):
    """ Base API Exception to provide option to fail silently"""

    def __init__(self, *args, **kwargs):
        super(BaseAPIException, self).__init__(*args, **kwargs)


class BadRequest(BaseAPIException):
    """Request method is invalid."""

    status_code = 400
    default_detail = 'Request details are invalid.'
    default_code = 'bad_request'
    send_to_sentry = True


class UnauthorizedAccess(BaseAPIException):
    """user Authorization failed."""

    status_code = 401
    default_detail = 'User is not authorized to access.'
    default_code = 'unauthorized_access'
    send_to_sentry = False
