from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Employee full name")
    email: EmailStr = Field(..., description="Employee work email address")
    department: str = Field(..., min_length=1, max_length=100, description="Employee department")
    role: str = Field(..., min_length=1, max_length=100, description="Job title / role")
    salary: float = Field(..., gt=0, description="Annual salary, must be greater than 0")


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100, description="Employee full name")
    email: Optional[EmailStr] = Field(None, description="Employee work email address")
    department: Optional[str] = Field(None, min_length=1, max_length=100, description="Employee department")
    role: Optional[str] = Field(None, min_length=1, max_length=100, description="Job title / role")
    salary: Optional[float] = Field(None, gt=0, description="Annual salary, must be greater than 0")


class EmployeeResponse(EmployeeBase):
    id: int = Field(..., description="Unique employee identifier")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "department": "Engineering",
                "role": "Software Engineer",
                "salary": 85000.0,
            }
        }
    }
