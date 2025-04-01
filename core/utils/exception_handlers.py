from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    """
    Manipulador de exceções personalizado para a API
    """
    # Primeiro chama o manipulador padrão para obter a resposta padrão
    response = exception_handler(exc, context)

    if response is None:
        if isinstance(exc, ValidationError):
            response = Response({
                'error': 'Validation Error',
                'detail': exc.messages
            }, status=status.HTTP_400_BAD_REQUEST)
        elif isinstance(exc, Http404):
            response = Response({
                'error': 'Not Found',
                'detail': str(exc)
            }, status=status.HTTP_404_NOT_FOUND)
        elif isinstance(exc, Exception):
            response = Response({
                'error': 'Internal Server Error',
                'detail': str(exc)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if response is not None:
        # Adiciona mais informações à resposta
        response.data = {
            'status_code': response.status_code,
            'error': response.data.get('detail', str(exc)) if isinstance(response.data, dict) else str(exc),
            'detail': response.data if isinstance(response.data, dict) else {'message': response.data}
        }

    return response 