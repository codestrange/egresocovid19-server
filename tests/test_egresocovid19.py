from random import choice, randrange

from egresocovid19.api.v1.auth import get_current_active_user
from egresocovid19.database import UserEntity
from egresocovid19.main import api_v1, app
from egresocovid19.static.municipality_codes import municipality_codes
from fastapi.testclient import TestClient
from mimesis import Address, Person


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


def test_create_patient():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        fake_address = Address()

        data = {
            "firstname": fake_person.first_name(),
            "lastname": fake_person.last_name(),
            "ci": fake_person.identifier("###########"),
            "age": fake_person.age(),
            "sex": randrange(3),
            "skinColor": randrange(3),
            "bloodType": randrange(8),
            "address": fake_address.address(),
            "polyclinic": fake_person.full_name(),
            "surgery": fake_person.full_name(),
            "popularCouncil": fake_person.full_name(),
            "neighborhood": fake_address.region(),
            "blockNumber": randrange(100),
            "personalPathologicalHistory": [
                {
                    "name": fake_person.full_name(),
                    "treatments": fake_person.full_name(),
                }
                for _ in range(randrange(1, 10))
            ],
            "familyPathologicalHistory": [
                {
                    "name": fake_person.full_name(),
                    "treatments": fake_person.full_name(),
                }
                for _ in range(randrange(1, 10))
            ],
            "municipalityCode": choice(list(municipality_codes.keys())),
        }
        response = client.post("api/v1/patients", json=data)
        assert response.status_code == 200
