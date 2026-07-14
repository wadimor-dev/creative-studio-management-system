from fastapi import status
from app.exceptions.base import AppException

class AuthException(AppException):
    pass

class InvalidCredentialException(AuthException):
    def __init__(self, message="Invalid credentials"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class ExpiredTokenException(AuthException):
    def __init__(self, message="Token has expired"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class PermissionDeniedException(AuthException):
    def __init__(self, message="Permission denied"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)
