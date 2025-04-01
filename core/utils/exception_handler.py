from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import IntegrityError
from django.http import Http404


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'status': 'error',
            'code': response.status_code,
            'message': 'Ocorreu um erro',
            'details': response.data
        }
        response.data = error_data
        return response

    error_response = {
        'status': 'error',
        'message': str(exc),
        'details': None
    }

    if isinstance(exc, ValidationError):
        error_response['code'] = status.HTTP_400_BAD_REQUEST
        error_response['message'] = 'Erro de validação'
        error_response['details'] = exc.message_dict if hasattr(exc, 'message_dict') else str(exc)
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, IntegrityError):
        error_response['code'] = status.HTTP_400_BAD_REQUEST
        error_response['message'] = 'Erro de integridade do banco de dados'
        return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

    elif isinstance(exc, PermissionDenied):
        error_response['code'] = status.HTTP_403_FORBIDDEN
        error_response['message'] = 'Permissão negada'
        return Response(error_response, status=status.HTTP_403_FORBIDDEN)

    elif isinstance(exc, Http404):
        error_response['code'] = status.HTTP_404_NOT_FOUND
        error_response['message'] = 'Recurso não encontrado'
        return Response(error_response, status=status.HTTP_404_NOT_FOUND)

    error_response['code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_response['message'] = 'Erro interno do servidor'
    return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)