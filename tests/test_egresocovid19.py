from random import choice, randrange
from typing import Any, Dict, cast

import pytest
from egresocovid19.api.v1.auth import get_current_active_user
from egresocovid19.database import UserEntity
from egresocovid19.main import api_v1, app
from egresocovid19.static.municipality_codes import municipality_codes
from fastapi.testclient import TestClient
from mimesis import Address, Person

shared_dict: Dict[str, Any] = {}


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
        json = response.json()
        assert json
        assert isinstance(json, dict)
        assert json.get("id")
        assert isinstance(json.get("id"), str)
        shared_dict["patient_id"] = json.get("id")


@pytest.mark.depends(on=[test_create_patient.__name__])
def test_get_patient():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/{patient_id}")
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, dict)
        assert json.get("id") == patient_id
        assert json.get("firstname")
        assert json.get("lastname")
        assert json.get("ci")
        assert isinstance(json.get("firstname"), str)
        assert isinstance(json.get("lastname"), str)
        assert isinstance(json.get("ci"), str)
        shared_dict["patient_firstname"] = json.get("firstname")
        shared_dict["patient_lastname"] = json.get("lastname")
        shared_dict["patient_ci"] = json.get("ci")


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_get_patients_by_firstname():
    assert shared_dict.get("patient_id")
    assert shared_dict.get("patient_firstname")
    patient_id = shared_dict.get("patient_id")
    patient_firstname = shared_dict.get("patient_firstname")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/search/{patient_firstname}")
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, list)
        assert all((isinstance(item, dict) for item in json))
        assert any((item.get("id") == patient_id for item in json))


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_get_patients_by_lastname():
    assert shared_dict.get("patient_id")
    assert shared_dict.get("patient_lastname")
    patient_id = shared_dict.get("patient_id")
    patient_lastname = shared_dict.get("patient_lastname")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/search/{patient_lastname}")
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, list)
        assert all((isinstance(item, dict) for item in json))
        assert any((item.get("id") == patient_id for item in json))


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_get_patients_by_ci():
    assert shared_dict.get("patient_id")
    assert shared_dict.get("patient_ci")
    patient_id = shared_dict.get("patient_id")
    patient_ci = shared_dict.get("patient_ci")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/search/{patient_ci}")
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, list)
        assert all((isinstance(item, dict) for item in json))
        assert any((item.get("id") == patient_id for item in json))


@pytest.mark.depends(on=[test_create_patient.__name__])
def test_edit_patient_basic():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "firstname": fake_person.first_name(),
        }
        response = client.put(f"api/v1/patients/{patient_id}", json=data)
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, dict)
        assert json.get("id") == patient_id
        assert json.get("firstname")
        assert isinstance(json.get("firstname"), str)
        shared_dict["patient_firstname"] = json.get("firstname")


@pytest.mark.depends(on=[test_create_patient.__name__])
def test_edit_patient_egreso():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "antibiotics": [fake_person.title()],
        }
        response = client.put(f"api/v1/patients/{patient_id}/egreso", json=data)
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, dict)
        assert json.get("id") == patient_id
        assert json.get("dischargeOfPositiveCasesOfCovid19")
        assert isinstance(json.get("dischargeOfPositiveCasesOfCovid19"), dict)
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get(
            "antibiotics"
        )
        assert (
            cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get("antibiotics")
            == data["antibiotics"]
        )
