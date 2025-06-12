from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))

# import pytest
# from httpx import AsyncClient, ASGITransport
# from backend.core_service.app.api.v1.user import router


# @pytest.mark.asyncio
# async def test_create_user():
#     test_data = {
#         "login": "user@example.com",
#         "password": "mypassword123"
#     }

#     async with AsyncClient(transport=ASGITransport(app=router), base_url="http://test") as ac:
#         response = await ac.post("/login", json=test_data)

#         # Проверки
#         assert response.status_code == 200  # или 201 для создания
#         print(response.json())


# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Импортируем ВСЕ модели перед созданием таблиц
# from backend.core_service.app.models.models import Accounts, Events, TicketTypes, Tickets  # noqa: F401
# from backend.core_service.app.models.session import DBBaseModel, get_db

# # Создаём in-memory SQLite для тестов
# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Подключаем приложение
# from backend.core_service.app.main import app

# # Фикстура для БД
# @pytest.fixture()
# def test_db():
#     # Создаём все таблицы
#     DBBaseModel.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         DBBaseModel.metadata.drop_all(bind=engine)

# # Переопределяем зависимость
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

# def test_create_event(test_db):
#     response = client.post(
#         "/api/v1/auth/register",
#         json={
#             "login": "user@example.com",
#             "password": "mypassword123",
#             "name": "Витя"
#         }
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["login"] == "user@example.com"
#     assert "id" in data
