from pathlib import Path
import sys
from unittest.mock import MagicMock

sys.path.append(str(Path(__file__).parent.parent.parent))

from unittest.mock import AsyncMock

from fastapi import status
from httpx import AsyncClient
import pytest

from backend.core_service.app.api.v1 import user
from backend.core_service.app.schemas import GetUserInfoResponseDTO
from backend.core_service.app.services.user import get_service


@pytest.fixture
def mocked_user_service():
    mock = AsyncMock()
    mock.get_info_user.return_value = GetUserInfoResponseDTO(
        id=1, name="Test", email="test@example.com"
    )
    return mock


@pytest.mark.asyncio
async def test_get_user_info(mocked_user_service):
    user.router.dependency_overrides[get_service] = lambda: mocked_user_service

    async with AsyncClient(app=user.router, base_url="http://test") as ac:
        response = await ac.get(
            "/api/v1/auth",  # путь до твоей ручки
            cookies={"jwt_token": "mocked.jwt.token"},
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "name": "Test", "email": "test@example.com"}

    mocked_user_service.get_info_user.assert_awaited_once_with("mocked.jwt.token")

    user.router.dependency_overrides = {}  # очищаем переопределения
