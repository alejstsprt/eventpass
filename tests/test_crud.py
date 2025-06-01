# from unittest.mock import MagicMock

# from sqlalchemy.exc import IntegrityError
# import pytest

# # Файл для теста
# from backend.core_service.app.models.crud import user_registration


# class TestUserRegistration:
#     """Тест user_registration"""

#     def test_successful_registration(self) -> None:
#         """Проверка создается ли пользователь и получен ли айди пользователя"""
#         test_db = MagicMock()

#         fake_user = MagicMock()
#         fake_user.id = 1331

#         def fake_refresh(user):
#             user.id = fake_user.id

#         test_db.add.return_value = None
#         test_db.commit.return_value = None
#         test_db.refresh.side_effect = fake_refresh

#         result = user_registration(test_db, "mylogin", "mypassword")

#         assert result is not None, f"{result = } | Ожидалось что ответ не будет пустым."

#         assert result['user_id'] is not None, f"{result = } | Ожидалось что вернется айди при успешной регистрации."

#         assert isinstance(result['user_id'], int), f"{result = } | Ожидалось что айди будет int."

#     def test_double_registration(self) -> None:
#         """Проверка на повторную регистрацию на тот же логин"""
#         test_db = MagicMock()

#         test_db.add.return_value = None
#         test_db.commit.side_effect = IntegrityError("Пользователь уже есть", None, None)
#         test_db.refresh.return_value = None

#         result_reg_user_2 = user_registration(test_db, 'mylogin', 'mypassword')

#         assert result_reg_user_2['error'] is not None, f"{result_reg_user_2 = } | Ожидалось что будет ошибка повторной регистрации на тот же логин."

#     @pytest.mark.parametrize(
#         "login, password",
#         [
#             (None, None),
#             (None, "mypassword"),
#             ("mylogin", None),
#             ("", ""),
#             ("", "mypassword"),
#             ("mylogin", "")
#         ],
#         ids=[
#             "Без параметров (None)",
#             "Только пароль",
#             "Только логин",
#             "Без параметров (str)",
#             "Только пароль",
#             "Только логин"
#         ]
#     )
#     def test_no_data_registration(self, login, password) -> None:
#         """Проверка выдает ли ошибку при отсутствии входных данных"""
#         test_db = MagicMock()

#         result = user_registration(test_db, login, password)
#         assert result['error'] is not None, f"{result = } | Ожидалось что будет ошибка, ведь входных данных нету."

# # class TestIsExistsLogin:
# #     """Тест is_exists_login"""

# #     @pytest.mark.asyncio
# #     async def test_is_exists_login(self):
# #         """Ожидаем True, ведь пользователь 'login' есть в базе"""
# #         test_db = MagicMock()
# #         test_db.query.return_value.filter.return_value.first.return_value = True

# #         result = await is_exists_login(test_db, 'login')
# #         assert result['result'] is True, f"{result = } | Ожидалось что будет True"

# #     @pytest.mark.asyncio
# #     async def test_is_exists_login(self):
# #         """Ожидаем False, ведь пользователя 'login' нет в базе"""
# #         test_db = MagicMock()
# #         test_db.query.return_value.filter.return_value.first.return_value = False

# #         result = await is_exists_login(test_db, 'login')
# #         assert result['result'] is False, f"{result = } | Ожидалось что будет False"
