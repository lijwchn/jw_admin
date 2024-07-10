from datetime import datetime
from typing import List

from ninja import Router, Query
from ninja.pagination import paginate

from apps.rbac.models import Role
from apps.rbac.schemas import RoleOut, RoleFilterSchema, RoleIn, RoleMenuIn, RoleUpdateIn
from core.my_pagination import MyPagination
from utils.base_curd import get_by_id, retrieve, create, delete_by_id, update_by_id
from utils.usual import get_user_info_from_token

router = Router()


@router.get("/role/{role_id}", response=RoleOut)
def get_role_by_id(request, role_id: int):
    """
    查询单个角色
    """
    data = get_by_id(Role, role_id)
    return data


@router.get("/role", response=List[RoleOut])
@paginate(MyPagination)
def list_role(request, filters: RoleFilterSchema = Query(...)):
    """
    查询角色列表
    当存在 bool 值作为过滤条件时，需要指定查询模式为 exact ,否则会查不出数据，因为查询条件为 like '%True%'
    """
    query_type = {"status": "exact"}
    query_set = retrieve(request, Role, filters, query_type)
    return query_set


@router.post("/role")
def create_role(request, payload: RoleIn):
    """
    创建角色
    """
    data = create(request, payload, Role)
    return data.id


@router.delete("/role/{role_id}")
def delete_role(request, role_id: int):
    """
    根据id删除角色
    同时 django 模型会自动删除和角色表相关联表中的数据
    """
    data = delete_by_id(Role, role_id)
    return data.id


@router.put("/role")
def update_role(request, payload: RoleUpdateIn):
    role_id = payload.id
    data = update_by_id(request, data=payload, model=Role, model_id=role_id)
    return data.id


@router.post("/role/{role_id}/menu")
def update_role_menu(request, role_id: int, payload: RoleMenuIn):
    """
    给角色分配权限，新增 & 修改 & 删除共用这个接口
    """
    operate_user_info = get_user_info_from_token(request)
    role = get_by_id(Role, role_id)
    role.menu.set(payload.menu_ids)
    # role.menu_button.set(payload.menu_button_ids)
    if operate_user_info is not None:
        # 为更新的数据添加修改者信息
        role.updater = operate_user_info.username
        role.update_time = datetime.now()
    role.save()
    return role.id
