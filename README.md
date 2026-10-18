# Employee Management API (API Key Protected)

A robust RESTful API built with **FastAPI** and **Pydantic** to manage employee records with API Key protection.

---

## Features

- **API Key Security**: Endpoints are secured with an `X-API-Key` header (`super30-secret-key` or customizable via `API_KEY` env var).
  - Missing key returns `401 Unauthorized`.
  - Incorrect key returns `403 Forbidden`.
- **Pydantic Validation**:
  - `name`: String, non-empty (1–100 chars).
  - `email`: Valid RFC email format, uniqueness enforced.
  - `department`: String (1–100 chars).
  - `role`: String (1–100 chars).
  - `salary`: Numeric, strictly greater than 0 (`gt=0`).
- **Full CRUD Endpoints**:
  - `GET /employees` (with optional `department` and `search` query filters)
  - `GET /employees/{employee_id}`
  - `POST /employees`
  - `PUT /employees/{employee_id}`
  - `DELETE /employees/{employee_id}`
- **Interactive Swagger Documentation** at `/docs`.
- **Automated Pytest Suite** verifying all auth rules, validation constraints, and CRUD flows.

---

## Setup & Running

### 1. Activate Virtual Environment & Install Dependencies

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Start the API Server

```powershell
uvicorn main:app --reload --port 8000
```

The API will be accessible at `http://127.0.0.1:8000`.

- Interactive Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc alternative docs: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Authentication

Supply the API key in the `X-API-Key` request header:

```http
X-API-Key: super30-secret-key
```

### Auth Responses:
- **Missing Header**: `401 Unauthorized`
  ```json
  {"detail": "Missing API Key. Please provide the 'X-API-Key' header."}
  ```
- **Invalid Header**: `403 Forbidden`
  ```json
  {"detail": "Forbidden: Invalid API Key provided."}
  ```

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/` | API status & welcome message | No |
| `GET` | `/health` | Health check endpoint | No |
| `GET` | `/employees` | List all employees (supports `?department=` & `?search=`) | Yes |
| `GET` | `/employees/{employee_id}` | Retrieve specific employee by ID | Yes |
| `POST` | `/employees` | Create a new employee | Yes |
| `PUT` | `/employees/{employee_id}` | Update existing employee fields | Yes |
| `DELETE`| `/employees/{employee_id}` | Remove employee by ID | Yes |

---

## Running Tests

Run the test suite with:

```powershell
pytest -v
```