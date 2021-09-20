from typing import Any, Dict

import pytest
from egresocovid19.cli import app as cli_app
from egresocovid19.main import api_v1, app
from fastapi.testclient import TestClient
from mimesis import Cryptographic, Person
from typer.testing import CliRunner

shared_dict: Dict[str, Any] = {}

runner = CliRunner()


def test_for_create_user():
    fake_person = Person()
    email = fake_person.email()
    password = fake_person.password()
    input = f"{fake_person.full_name()}\n"
    input += f"{email}\n"
    input += f"{fake_person.telephone()}\n"
    input += f"{password}\n{password}\n"
    input += "y\ny\nN\n"
    result = runner.invoke(cli_app, ["users", "create"], input=input)
    assert result.exit_code == 0
    shared_dict["username"] = email
    shared_dict["password"] = password


@pytest.mark.depends(on=[test_for_create_user.__name__])
def test_get_provinces():
    api_v1.dependency_overrides = {}
    username = shared_dict.get("username")
    password = shared_dict.get("password")
    assert username
    assert password
    with TestClient(app) as client:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 200
        json = response.json()
        print(json)
        assert json
        assert isinstance(json, dict)
        assert json.get("access_token")
        assert isinstance(json.get("access_token"), str)
        response = client.get(
            "/api/v1/provinces",
            headers={"Authorization": f"Bearer {json.get('access_token')}"},
        )
        assert response.status_code == 200
        assert len(response.json()) == 16


def test_for_create_user_disabled():
    fake_person = Person()
    email = fake_person.email()
    password = fake_person.password()
    input = f"{fake_person.full_name()}\n"
    input += f"{email}\n"
    input += f"{fake_person.telephone()}\n"
    input += f"{password}\n{password}\n"
    input += "y\ny\ny\n"
    result = runner.invoke(cli_app, ["users", "create"], input=input)
    assert result.exit_code == 0
    shared_dict["username_disabled"] = email
    shared_dict["password_disabled"] = password


@pytest.mark.depends(on=[test_for_create_user_disabled.__name__])
def test_get_provinces_with_disabled_user():
    api_v1.dependency_overrides = {}
    username = shared_dict.get("username_disabled")
    password = shared_dict.get("password_disabled")
    assert username
    assert password
    print(username)
    print(password)
    with TestClient(app) as client:
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 200
        json = response.json()
        print(json)
        assert json
        assert isinstance(json, dict)
        assert json.get("access_token")
        assert isinstance(json.get("access_token"), str)
        response = client.get(
            "/api/v1/provinces",
            headers={"Authorization": f"Bearer {json.get('access_token')}"},
        )
        assert response.status_code == 401


def test_get_provinces_with_invalid_token():
    api_v1.dependency_overrides = {}
    with TestClient(app) as client:
        fake = Cryptographic()
        response = client.get(
            "/api/v1/provinces",
            headers={"Authorization": f"Bearer {fake.token_urlsafe()}"},
        )
        assert response.status_code == 401
