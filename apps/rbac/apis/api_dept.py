from typing import List

from ninja import Router, Query
from ninja.pagination import paginate

from apps.rbac.models import Dept
from apps.rbac.schemas import DeptIn, DeptOut, DeptFilterSchema
from core.my_pagination import MyPagination
from utils.base_curd import get_by_id, retrieve, create, delete_by_id, update_by_id

router = Router()


@router.get("/dept/{dept_id}", response=DeptOut)
def get_dept_by_id(request, dept_id: int):
    data = get_by_id(Dept, dept_id)
    return data


@router.get("/dept", response=List[DeptOut])
@paginate(MyPagination)
def list_dept(request, filters: DeptFilterSchema = Query(...)):
    """
    获取部门列表。
    参数:
    - request: 请求对象，包含请求的相关信息。
    - filters: 部门过滤条件，用于筛选部门列表。
    """
    query_set = retrieve(request, Dept, filters)
    return query_set


@router.post("/dept")
def create_dept(request, payload: DeptIn):
    """
    创建部门。
    参数:
    - request: 请求对象，包含请求的相关信息。
    - payload: 部门信息的输入模型，用于解析请求体中的部门。

    返回值:
    - int
    """
    data = create(request, payload, Dept)
    return data.id


@router.put("/dept/{dept_id}")
def update_dept(request, dept_id: int, payload: DeptIn):
    """
    更新部门
    """
    data = update_by_id(request, payload, Dept, dept_id)
    return data.id


@router.delete("/dept/{dept_id}")
def delete_dept(request, dept_id: int):
    """
    删除部门
    """
    data = delete_by_id(Dept, dept_id)
    return data.id
