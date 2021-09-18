from egresocovid19.api.v1.auth import get_current_active_user
from egresocovid19.database import UserEntity
from egresocovid19.main import api_v1, app
from fastapi.testclient import TestClient


async def mock_get_current_active_user() -> UserEntity:
    return UserEntity(
        name="Test client",
        email="test@gmail.com",
        phone="+0000000000",
        hashed_password="hashed_password",
        email_confirmed=True,
        phone_confirmed=True,
        disabled=False,
    )


def test_provinces():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get("/api/v1/provinces")
        assert response.status_code == 200
        assert len(response.json()) == 16
