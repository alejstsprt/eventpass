import pytest

"""Файл для теста"""
from backend.core_service.app.security.hashing import hash_password, verify_password


class TestHashPassword():
    """Тест hash_password"""

    def test_type_return(self):
        """Возвращается ли строка с хешем"""
        result = hash_password('mypassword')
        assert isinstance(result, str), f"{result = } | Ожидалось что хеш будет str"

    def test_no_data(self):
        """Возвращается ли None если не указать входные данные"""
        result = hash_password('')
        assert not result, f"{result = } | Ожидалось что вернет None, ведь входных данных не было"

class TestVerifyPassword():
    """Тест verify_password"""

    def test_true_password(self):
        """Возвращается ли True, если пароль правильный"""
        my_hash = hash_password('mypassword')
        assert verify_password('mypassword', my_hash) is True, f"{verify_password('mypassword', my_hash) = } | Ожидалось что будет True"

    def test_false_password(self):
        """Возвращается ли False, если пароль неправильный"""
        my_hash = hash_password('mypassword')
        assert verify_password('mypassword2', my_hash) is False, f"{verify_password('mypassword', my_hash) = } | Ожидалось что будет False"

    @pytest.mark.parametrize(
        'plain_password, hashed_password',
        [
            ('', ''),
            ('', 'mypassword'),
            ('mypassword', '')
        ],
        ids=[
            'Все данные не указаны',
            'Не указан пароль',
            'Не указан хеш'
        ]
    )
    def test_no_data(self, plain_password, hashed_password):
        """Возвращается ли False, если входные данные указаны не все"""
        result = verify_password(plain_password, hashed_password)
        assert result is False, f"{result = } | Ожидалось что будет False"