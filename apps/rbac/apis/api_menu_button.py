"""
权限管理没有应用到菜单按钮这一级，这个文件的代码没有用到
"""

from ninja import Router

from apps.rbac.models import MenuButton
from apps.rbac.schemas import MenuButtonIn, MenuButtonOut
from utils.base_curd import create, get_by_id, delete_by_id, update_by_id

router = Router()


@router.get("/menu_button/{menu_button_id}", response=MenuButtonOut)
def get_menu_button_by_id(request, menu_button_id: int):
    """
    获取单个菜单按钮的详情
    """
    data = get_by_id(MenuButton, menu_button_id)
    return data


@router.post("/menu_button")
def create_menu_button(request, payload: MenuButtonIn):
    """
    创建菜单按钮
    """
    # 将parent_id赋值给menu，兼容前端的传参
    payload.menu = payload.parent_id
    data = create(request, payload, MenuButton)
    return data.id


@router.put("/menu_button")
def update_menu_button(request, payload: MenuButtonIn):
    """
    更新菜单按钮
    """
    payload.menu = payload.parent_id
    data = update_by_id(request, payload, MenuButton, payload.id)
    return data.id


@router.delete("/menu_button/{menu_button_id}")
def delete_menu_button(request, menu_button_id: int):
    """
    删除单个菜单按钮
    """
    data = delete_by_id(MenuButton, menu_button_id)
    return data.id
