from egresocovid19.api.v1.auth import get_current_active_user
from egresocovid19.database import UserEntity
from egresocovid19.main import api_v1, app
from fastapi.testclient import TestClient
from mimesis import Text
from pydantic import EmailStr


async def mock_get_current_active_user() -> UserEntity:
    return UserEntity(
        name="Test client",
        email=EmailStr("test@gmail.com"),
        phone="+0000000000",
        hashed_password="hashed_password",
        email_confirmed=True,
        phone_confirmed=True,
        disabled=False,
    )


def test_get_polyclinics():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/polyclinics/{query}")
        assert response.status_code == 200


def test_get_surgeries():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/surgeries/{query}")
        assert response.status_code == 200


def test_get_popular_councils():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/popular_councils/{query}")
        assert response.status_code == 200


def test_get_neighborhoods():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/neighborhoods/{query}")
        assert response.status_code == 200


def test_get_pathologicals():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/pathologicals/{query}")
        assert response.status_code == 200


def test_get_default_pathologicals():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get("api/v1/autocomplete/default_pathologicals")
        assert response.status_code == 200


def test_get_antibiotics():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/antibiotics/{query}")
        assert response.status_code == 200


def test_get_another_vaccines_against_covid():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(
            f"api/v1/autocomplete/another_vaccines_against_covid/{query}"
        )
        assert response.status_code == 200


def test_get_others_aftermaths():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/others_aftermaths/{query}")
        assert response.status_code == 200


def test_get_symptoms():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_text = Text()
        query = fake_text.word()
        response = client.get(f"api/v1/autocomplete/symptoms/{query}")
        assert response.status_code == 200


def test_get_default_symptoms():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get("api/v1/autocomplete/default_symptoms")
        assert response.status_code == 200
