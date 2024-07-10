from datetime import date
from typing import Optional

from ninja import Schema, ModelSchema

# from core.my_pagination import PaginationInputSchema
from .models import Employee


class EmployeeIn(Schema):
    first_name: str
    last_name: str
    department_id: int = None
    birthdate: date = None


class EmployeeOut(ModelSchema):
    class Meta:
        model = Employee
        exclude = ["birthdate"]


class EmployeeFilterSchema(Schema):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
