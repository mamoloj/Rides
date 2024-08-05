import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)


    # If the response is None, it means DRF didn't handle this exception
    if response is None:
        return Response(
            {'detail': exc},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # Customize the response format for ValidationError
    if isinstance(exc, ValidationError):
        # Here, we manually build the error response
        response.data = {
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': 'Validation Error',
            'detail': exc.detail
        }
        response.status_code = status.HTTP_400_BAD_REQUEST

    return response
