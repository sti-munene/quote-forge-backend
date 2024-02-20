from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler


class CustomApiException(APIException):
    # Public fields
    detail = None
    status_code = None

    # create constructor
    def __init__(self, status_code, message):
        # Override public fields
        CustomApiException.status_code = status_code
        CustomApiException.detail = message
