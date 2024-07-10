from typing import List

from ninja import Query
from ninja import Router
from ninja.pagination import paginate

from core.my_pagination import MyPagination
from utils.base_curd import retrieve, delete_by_id, get_by_id, create, update_by_id
from .models import Employee
from .schemas import EmployeeIn, EmployeeOut, EmployeeFilterSchema

router = Router()


@router.get(
    "/employees/{employee_id}", response=EmployeeOut, description="根据id获取员工信息"
)
def get_employee_by_id(request, employee_id: int):
    data = get_by_id(Employee, employee_id)
    # 这里直接返回data，会被MyNinjaAPI中的create_response方法拦截，并且会自动被EmployeeOut序列化
    return data


@router.get("/employees", response=List[EmployeeOut], description="获取员工列表")
@paginate(MyPagination)
def list_employees(request, filters: EmployeeFilterSchema = Query(...)):
    query_set = retrieve(request, Employee, filters)
    return query_set


@router.post("/create_employees")
def create_employee(request, payload: EmployeeIn):
    employee = create(request, data=payload, model=Employee)
    return employee.id


@router.put("/employees/{employee_id}")
def update_employee(request, employee_id: int, payload: EmployeeIn):
    employee = update_by_id(request, data=payload, model=Employee, model_id=employee_id)
    # return standard_response(data=data)
    return employee.id


@router.delete("/employees/{employee_id}")
def delete_employee(request, employee_id: int):
    employee = delete_by_id(Employee, employee_id)
    return employee.id
