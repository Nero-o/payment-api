from rest_framework import status


class BaseAPIException(Exception):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = "Ocorreu um erro inesperado."
    
    def __init__(self, message=None, details=None):
        self.message = message or self.default_message
        self.details = details
        super().__init__(self.message)


class BadRequestException(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = "Requisição inválida."


class NotFoundException(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = "Recurso não encontrado."


class UnauthorizedException(BaseAPIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_message = "Não autorizado."


class ForbiddenException(BaseAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_message = "Acesso proibido."


class ConflictException(BaseAPIException):
    status_code = status.HTTP_409_CONFLICT
    default_message = "Conflito de recursos."


class InsufficientFundsException(BadRequestException):
    default_message = "Saldo insuficiente"