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
    """[all] Ошибка неверные данные"""
    def __init__(self, detail="Неверные данные"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class LoginError(ValidationError):
    """[NotAll] Ошибка Неверный логин"""
    def __init__(self):
        super().__init__(detail = "Неверный логин")

class PasswordError(ValidationError):
    """[NotAll] Ошибка Неверный пароль"""
    def __init__(self):
        super().__init__(detail = "Неверный пароль")

class TokenError(ValidationError):
    """[NotAll] Ошибка Неверный токен"""
    def __init__(self):
        super().__init__(detail = "Неверный токен")

class NoTokenError(ValidationError):
    """[NotAll] Ошибка Токен отсутствует"""
    def __init__(self):
        super().__init__(detail = "Токен отсутствует")


# HTTP_401_UNAUTHORIZED

