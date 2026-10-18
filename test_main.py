import pytest
from fastapi.testclient import TestClient

from auth import EXPECTED_API_KEY
from main import app
from routes import employees_db

client = TestClient(app)

VALID_HEADERS = {"X-API-Key": EXPECTED_API_KEY}
INVALID_HEADERS = {"X-API-Key": "wrong-secret-key"}


@pytest.fixture(autouse=True)
def reset_db():
    employees_db.clear()
    employees_db.update(
        {
            1: {
                "id": 1,
                "name": "Alice Smith",
                "email": "alice.smith@example.com",
                "department": "Engineering",
                "role": "Backend Engineer",
                "salary": 92000.0,
            },
            2: {
                "id": 2,
                "name": "Bob Johnson",
                "email": "bob.johnson@example.com",
                "department": "Design",
                "role": "UI/UX Designer",
                "salary": 78000.0,
            },
        }
    )


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]


def test_auth_missing_api_key():
    response = client.get("/employees")
    assert response.status_code == 401
    assert "Missing API Key" in response.json()["detail"]


def test_auth_invalid_api_key():
    response = client.get("/employees", headers=INVALID_HEADERS)
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]


def test_get_employees_success():
    response = client.get("/employees", headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Alice Smith"


def test_get_employees_filter_department():
    response = client.get("/employees?department=Engineering", headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["department"] == "Engineering"


def test_get_employee_by_id_success():
    response = client.get("/employees/1", headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["email"] == "alice.smith@example.com"


def test_get_employee_by_id_not_found():
    response = client.get("/employees/999", headers=VALID_HEADERS)
    assert response.status_code == 404


def test_create_employee_success():
    payload = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "department": "DevOps",
        "role": "Cloud Architect",
        "salary": 115000.0,
    }
    response = client.post("/employees", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["id"] is not None


def test_create_employee_validation_error():
    # Negative salary and invalid email
    payload = {
        "name": "",
        "email": "not-an-email",
        "department": "DevOps",
        "role": "Cloud Architect",
        "salary": -500,
    }
    response = client.post("/employees", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 422


def test_create_employee_duplicate_email():
    payload = {
        "name": "Duplicate Alice",
        "email": "alice.smith@example.com",
        "department": "Engineering",
        "role": "Engineer",
        "salary": 70000.0,
    }
    response = client.post("/employees", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]


def test_update_employee_success():
    payload = {
        "role": "Lead Engineer",
        "salary": 105000.0,
    }
    response = client.put("/employees/1", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "Lead Engineer"
    assert data["salary"] == 105000.0
    assert data["name"] == "Alice Smith"


def test_update_employee_not_found():
    payload = {"role": "Lead Engineer"}
    response = client.put("/employees/999", json=payload, headers=VALID_HEADERS)
    assert response.status_code == 404


def test_delete_employee_success():
    response = client.delete("/employees/1", headers=VALID_HEADERS)
    assert response.status_code == 200

    # Ensure it is gone
    get_res = client.get("/employees/1", headers=VALID_HEADERS)
    assert get_res.status_code == 404


def test_delete_employee_not_found():
    response = client.delete("/employees/999", headers=VALID_HEADERS)
    assert response.status_code == 404
