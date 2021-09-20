from typing import Any, Dict

import pytest
from egresocovid19.cli import app as cli_app
from egresocovid19.main import api_v1, app
from fastapi.testclient import TestClient
from mimesis import Person
from typer.testing import CliRunner

shared_dict: Dict[str, Any] = {}

runner = CliRunner()


def test_cli_users_create():
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


def test_auth_token_invalid_grant_type():
    api_v1.dependency_overrides = {}
    with TestClient(app) as client:
        data = {
            "grant_type": "invalid_grant_type",
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 400


@pytest.mark.depends(on=[test_cli_users_create.__name__])
def test_auth_token_access():
    api_v1.dependency_overrides = {}
    username = shared_dict.get("username")
    password = shared_dict.get("password")
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
        assert json.get("refresh_token")
        assert isinstance(json.get("access_token"), str)
        assert isinstance(json.get("refresh_token"), str)
        shared_dict["access_token"] = json.get("access_token")
        shared_dict["refresh_token"] = json.get("refresh_token")


def test_auth_token_access_without_username_and_password():
    api_v1.dependency_overrides = {}
    with TestClient(app) as client:
        data = {
            "grant_type": "password",
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 400


@pytest.mark.depends(on=[test_cli_users_create.__name__])
def test_auth_token_access_error_username():
    api_v1.dependency_overrides = {}
    password = shared_dict.get("password", None)
    assert password
    with TestClient(app) as client:
        fake_person = Person()
        data = {
            "grant_type": "password",
            "username": fake_person.email(),
            "password": password,
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 401


@pytest.mark.depends(on=[test_cli_users_create.__name__])
def test_auth_token_access_error_password():
    api_v1.dependency_overrides = {}
    username = shared_dict.get("username", None)
    assert username
    with TestClient(app) as client:
        fake_person = Person()
        data = {
            "grant_type": "password",
            "username": username,
            "password": fake_person.password(),
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 401


@pytest.mark.depends(on=[test_auth_token_access.__name__])
def test_auth_token_refresh():
    api_v1.dependency_overrides = {}
    refresh_token = shared_dict.get("refresh_token", None)
    assert refresh_token
    with TestClient(app) as client:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 200
        json = response.json()
        assert json
        assert isinstance(json, dict)
        assert json.get("access_token")
        assert json.get("refresh_token")
        assert isinstance(json.get("access_token"), str)
        assert isinstance(json.get("refresh_token"), str)
        shared_dict["access_token"] = json.get("access_token")
        shared_dict["refresh_token"] = json.get("refresh_token")


def test_auth_token_refresh_incorrect():
    api_v1.dependency_overrides = {}
    with TestClient(app) as client:
        data = {
            "grant_type": "refresh_token",
            "refresh_token": "incorrect_refresh_token",
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 401


def test_auth_token_refresh_without_refresh_token():
    api_v1.dependency_overrides = {}
    with TestClient(app) as client:
        data = {
            "grant_type": "refresh_token",
        }
        response = client.post("api/v1/auth/token", data=data)
        assert response.status_code == 400
