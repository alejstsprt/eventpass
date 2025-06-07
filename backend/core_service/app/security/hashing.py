from core.exceptions import ValidationError
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__rounds=12,  # Количество раундов (12-15 оптимально). Лучше всего 12, а то слишком долго будет, да и пользы нету если больше
    bcrypt__ident="2b",  # Используем современную версию bcrypt
    deprecated="auto",  # Автоматически помечает устаревшие методы
)


def hash_password(password: str) -> str:
    """
    Функция для хеширования пароля

    Args:
        password (str): Пароль в чистом виде

    Returns:
        str: Хеш пароля
    """
    if not password:
        raise ValidationError()

    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Функция для проверки соответствия паролей

    Args:
        plain_password (str): Пароль в чистом виде
        hashed_password (str): Хеш пароля из базы данных

    Returns:
        bool: Результат проверки
    """
    if not plain_password or not hashed_password:
        return False

    return pwd_context.verify(plain_password, hashed_password)
