from fastapi import HTTPException, status


# class ValidationError2(HTTPException):
#     """Ошибка при неверно введенных данных"""
#     def __init__(self, detail: str = "Некорректные данные"):
#         super().__init__(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=detail
#         )

class InternalServerError(HTTPException):
    """Ошибка для неожиданных серверных сбоев"""
    def __init__(self, detail: str = "Внутренняя ошибка сервера"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )

class RegistrationFailedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Произошла ошибка при регистрации"
        )

class LoginAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Имя/Логин уже занят"
        )

class UnauthorizedException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Вы не авторизованы"
        )

class TokenMissingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен отсутствует"
        )

class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен"
        )







# HTTP_401_UNAUTHORIZED

class ValidationError(HTTPException):
    def __init__(self, detail="Неверные данные"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class LoginError(ValidationError):
    def __init__(self):
        super().__init__(detail = "Неверный логин")

class PasswordError(ValidationError):
    def __init__(self):
        super().__init__(detail = "Неверный пароль")