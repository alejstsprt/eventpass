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

    def __init__(self, detail: str = "Ошибка. Попробуйте позже.") -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail
        )


class RegistrationFailedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Произошла ошибка при регистрации",
        )


class LoginAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Логин уже занят"
        )


class NameAlreadyExistsException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Имя уже занято"
        )


class UnauthorizedException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Вы не авторизованы"
        )


class TokenMissingException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен отсутствует"
        )


class InvalidTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный токен",
        )


# HTTP_401_UNAUTHORIZED


class ValidationError(HTTPException):
    """[origin] Ошибка неверные данные"""

    def __init__(self, detail: str = "Неверные данные") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class LoginError(ValidationError):
    """[ValidationError] Ошибка Неверный логин"""

    def __init__(self) -> None:
        super().__init__(detail="Неверный логин")


class PasswordError(ValidationError):
    """[ValidationError] Ошибка Неверный пароль"""

    def __init__(self) -> None:
        super().__init__(detail="Неверный пароль")


class TokenError(ValidationError):
    """[ValidationError] Ошибка Неверный токен"""

    def __init__(self) -> None:
        super().__init__(detail="Неверный токен")


class NoTokenError(ValidationError):
    """[ValidationError] Ошибка Токен отсутствует"""

    def __init__(self) -> None:
        super().__init__(detail="Токен отсутствует")


class TicketTypeError(ValidationError):
    """[ValidationError] Ошибка Тип билета уже существует"""

    def __init__(self) -> None:
        super().__init__(
            detail="Данный тип билета для этого мероприятия уже существует"
        )


# HTTP_403_FORBIDDEN


class ForbiddenError(HTTPException):
    """[origin] Недостаточно прав для выполнения действия"""

    def __init__(
        self, detail: str = "Недостаточно прав для выполнения действия"
    ) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class ForbiddenUserError(ForbiddenError):
    """[ForbiddenError] Нет прав на удаление"""

    def __init__(self) -> None:
        super().__init__(detail="Нет прав на удаление")


class TicketLimitError(ForbiddenError):
    """[ForbiddenError] Нет прав на удаление"""

    def __init__(self) -> None:
        super().__init__(detail="Достигнут лимит билетов")
