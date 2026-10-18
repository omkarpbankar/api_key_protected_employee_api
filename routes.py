from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from auth import verify_api_key
from models import EmployeeCreate, EmployeeResponse, EmployeeUpdate

router = APIRouter(prefix="/employees", tags=["Employees"])

# In-memory storage seeded with sample data
employees_db: dict[int, dict] = {
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
    3: {
        "id": 3,
        "name": "Charlie Brown",
        "email": "charlie.brown@example.com",
        "department": "Marketing",
        "role": "Marketing Specialist",
        "salary": 65000.0,
    },
}

id_counter = 3


def get_next_id() -> int:
    global id_counter
    id_counter += 1
    return id_counter


@router.get(
    "",
    response_model=List[EmployeeResponse],
    summary="Get all employees",
    description="Retrieve a list of employees. Can filter by department or search by name. Protected by API key.",
)
async def get_employees(
    department: Optional[str] = Query(None, description="Filter by department name"),
    search: Optional[str] = Query(None, description="Search by employee name"),
    _: str = Depends(verify_api_key),
):
    results = list(employees_db.values())
    if department:
        results = [e for e in results if e["department"].lower() == department.strip().lower()]
    if search:
        results = [e for e in results if search.strip().lower() in e["name"].lower()]
    return results


@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Get employee by ID",
    description="Retrieve details of a single employee by their ID. Protected by API key.",
)
async def get_employee_by_id(
    employee_id: int,
    _: str = Depends(verify_api_key),
):
    if employee_id not in employees_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found.",
        )
    return employees_db[employee_id]


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Add a new employee record. Validates all fields using Pydantic. Protected by API key.",
)
async def create_employee(
    payload: EmployeeCreate,
    _: str = Depends(verify_api_key),
):
    # Verify email uniqueness
    for emp in employees_db.values():
        if emp["email"].lower() == payload.email.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Employee with email '{payload.email}' already exists.",
            )

    new_id = get_next_id()
    new_employee = {
        "id": new_id,
        "name": payload.name,
        "email": payload.email,
        "department": payload.department,
        "role": payload.role,
        "salary": payload.salary,
    }
    employees_db[new_id] = new_employee
    return new_employee


@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="Update an employee",
    description="Update fields of an existing employee. Protected by API key.",
)
async def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    _: str = Depends(verify_api_key),
):
    if employee_id not in employees_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found.",
        )

    current_data = employees_db[employee_id]
    update_data = payload.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided to perform an update.",
        )

    # Check email uniqueness if email is being updated
    if "email" in update_data:
        new_email = update_data["email"].lower()
        for emp_id, emp in employees_db.items():
            if emp_id != employee_id and emp["email"].lower() == new_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Employee with email '{update_data['email']}' already exists.",
                )

    current_data.update(update_data)
    employees_db[employee_id] = current_data
    return current_data


@router.delete(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an employee",
    description="Delete an employee record by their ID. Protected by API key.",
)
async def delete_employee(
    employee_id: int,
    _: str = Depends(verify_api_key),
):
    if employee_id not in employees_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found.",
        )

    deleted_employee = employees_db.pop(employee_id)
    return {
        "message": f"Employee {deleted_employee['name']} (ID: {employee_id}) successfully deleted.",
        "id": employee_id,
    }
