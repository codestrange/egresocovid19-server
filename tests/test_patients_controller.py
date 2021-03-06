from random import choice, randrange
from typing import Any, Dict, List, cast

import pytest
from beanie import PydanticObjectId
from egresocovid19.api.v1.auth import get_current_active_user
from egresocovid19.database import PatientEntity, UserEntity
from egresocovid19.main import api_v1, app
from egresocovid19.static.municipality_codes import municipality_codes
from egresocovid19.utils.run_sync import run_sync
from fastapi.testclient import TestClient
from mimesis import Address, Person
from pydantic import EmailStr

shared_dict: Dict[str, Any] = {}


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
        assert json.get("ci")
        assert json.get("personalPathologicalHistory")
        assert json.get("familyPathologicalHistory")
        assert isinstance(json.get("id"), str)
        assert isinstance(json.get("ci"), str)
        assert isinstance(json.get("personalPathologicalHistory"), list)
        assert isinstance(json.get("familyPathologicalHistory"), list)
        shared_dict["patient_id"] = json.get("id")
        shared_dict["patient_ci"] = json.get("ci")
        shared_dict["patient_personal_pathological_history"] = json.get(
            "personalPathologicalHistory"
        )
        shared_dict["patient_family_pathological_history"] = json.get(
            "familyPathologicalHistory"
        )


def test_create_patient_municipality_not_found():
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
            "municipalityCode": "99.99",
        }
        response = client.post("api/v1/patients", json=data)
        assert response.status_code == 404


@pytest.mark.depends(on=[test_create_patient.__name__])
def test_create_patient_with_existing_ci():
    assert shared_dict.get("patient_ci")
    patient_ci = shared_dict.get("patient_ci")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        fake_address = Address()
        data = {
            "firstname": fake_person.first_name(),
            "lastname": fake_person.last_name(),
            "ci": patient_ci,
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
        assert response.status_code == 400


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


def test_get_patient_not_found():
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/{PydanticObjectId()}")
        assert response.status_code == 404


@pytest.mark.depends(on=[test_create_patient.__name__])
def test_get_patient_municipality_not_found():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    patient = run_sync(PatientEntity.get_or_404(PydanticObjectId(patient_id)))
    patient.municipality_code = "99.99"
    run_sync(patient.save())
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        response = client.get(f"api/v1/patients/{patient_id}")
        assert response.status_code == 404
    patient.municipality_code = choice(list(municipality_codes.keys()))
    run_sync(patient.save())


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


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_edit_patient_basic():
    assert shared_dict.get("patient_id")
    assert shared_dict.get("patient_personal_pathological_history")
    assert shared_dict.get("patient_family_pathological_history")
    patient_id = shared_dict.get("patient_id")
    patient_personal_pathological_history = cast(
        List[Dict[str, str]], shared_dict.get("patient_personal_pathological_history")
    )
    patient_family_pathological_history = cast(
        List[Dict[str, str]], shared_dict.get("patient_family_pathological_history")
    )
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "firstname": fake_person.first_name(),
            "personalPathologicalHistory": [
                {
                    "name": fake_person.full_name(),
                    "treatments": fake_person.full_name(),
                }
                for _ in range(randrange(1, 10))
            ]
            + patient_personal_pathological_history,
            "familyPathologicalHistory": [
                {
                    "name": fake_person.full_name(),
                    "treatments": fake_person.full_name(),
                }
                for _ in range(randrange(1, 10))
            ]
            + patient_family_pathological_history,
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


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_edit_patient_basic_municipality_not_found():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "firstname": fake_person.first_name(),
            "municipalityCode": "99.99",
        }
        response = client.put(f"api/v1/patients/{patient_id}", json=data)
        assert response.status_code == 404


@pytest.mark.depends(on=[test_get_patient.__name__])
def test_edit_patient_basic_with_existing_ci():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    test_create_patient()
    assert shared_dict.get("patient_ci")
    patient_ci = shared_dict.get("patient_ci")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "firstname": fake_person.first_name(),
            "ci": patient_ci,
        }
        response = client.put(f"api/v1/patients/{patient_id}", json=data)
        assert response.status_code == 400


@pytest.mark.depends(on=[test_get_patient.__name__])
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
            "symptoms": [fake_person.title()],
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
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get(
            "antibiotics"
        ) == [item for item in data["antibiotics"]]
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get("symptoms")
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get(
            "symptoms"
        ) == [item for item in data["symptoms"]]


@pytest.mark.depends(on=[test_edit_patient_egreso.__name__])
def test_edit_patient_egreso_for_new_symptoms():
    assert shared_dict.get("patient_id")
    patient_id = shared_dict.get("patient_id")
    with TestClient(app) as client:
        api_v1.dependency_overrides[
            get_current_active_user
        ] = mock_get_current_active_user
        fake_person = Person()
        data = {
            "antibiotics": [fake_person.title()],
            "symptoms": [fake_person.title()],
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
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get(
            "antibiotics"
        ) == [item for item in data["antibiotics"]]
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get("symptoms")
        assert cast(dict, json.get("dischargeOfPositiveCasesOfCovid19")).get(
            "symptoms"
        ) == [item for item in data["symptoms"]]
