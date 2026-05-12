"""
Smart Tourism — Custom Exception Handler & Response Helpers
"""
import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Centralised exception handler.
    Wraps DRF's default handler output in a consistent envelope:
      { "success": false, "error": { "code": ..., "message": ..., "details": ... } }
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'error': {
                'code':    response.status_code,
                'message': _get_error_message(response),
                'details': response.data,
            }
        }
        response.data = error_data
    else:
        # Unhandled exceptions → 500
        logger.exception("Unhandled exception: %s", exc)
        response = Response(
            {
                'success': False,
                'error': {
                    'code':    500,
                    'message': 'Internal server error. Please try again later.',
                    'details': str(exc) if __import__('django.conf', fromlist=['settings']).settings.DEBUG else None,
                }
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return response


def _get_error_message(response) -> str:
    """Extract a human-readable message from the response data."""
    data = response.data
    if isinstance(data, dict):
        if 'detail' in data:
            return str(data['detail'])
        if 'non_field_errors' in data:
            return str(data['non_field_errors'][0])
        # first field error
        for key, val in data.items():
            if isinstance(val, list):
                return f"{key}: {val[0]}"
            return str(val)
    if isinstance(data, list) and data:
        return str(data[0])
    return "An error occurred."


# ── Reusable response builders ────────────────────────────────────────────────

def success_response(data=None, message="Success", status_code=status.HTTP_200_OK, **kwargs):
    """Standard success response envelope."""
    payload = {'success': True, 'message': message}
    if data is not None:
        payload['data'] = data
    payload.update(kwargs)
    return Response(payload, status=status_code)


def error_response(message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    """Standard error response envelope."""
    payload = {'success': False, 'message': message}
    if errors:
        payload['errors'] = errors
    return Response(payload, status=status_code)


def created_response(data=None, message="Created successfully"):
    return success_response(data=data, message=message, status_code=status.HTTP_201_CREATED)


def not_found_response(message="Resource not found"):
    return error_response(message=message, status_code=status.HTTP_404_NOT_FOUND)


def forbidden_response(message="You do not have permission to perform this action."):
    return error_response(message=message, status_code=status.HTTP_403_FORBIDDEN)