from datetime import datetime
from typing import List

from django.contrib.auth.hashers import make_password
from django.db import IntegrityError, transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from ninja import Router, Query
from ninja.pagination import paginate

from apps.rbac.models import Users
from apps.rbac.schemas import (
    UserOut,
    UserFilterSchema,
    CreateUserIn,
    SetPassword,
    UserDeleteIn,
    UpdateUserIn,
)
from core.my_pagination import MyPagination
from core.standard_response import standard_response
from utils.base_curd import get_by_id, retrieve, batch_delete_by_id
from utils.log_config import logger
from utils.usual import get_user_info_from_token, build_menu_tree

router = Router()


@router.get("/user/{user_id}", response=UserOut)
def get_user_by_id(request, user_id: int):
    """
    根据用户id查询
    """
    data = get_by_id(Users, user_id)
    return data


@router.get("/user", response=List[UserOut])
@paginate(MyPagination)
def list_users(request, filters: UserFilterSchema = Query(...)):
    """
    用户列表分页查询
    """
    query_types = {"status": "exact"}
    query_set = retrieve(request, Users, filters, query_types)
    return query_set


@router.post("/user")
def create_user(request, payload: CreateUserIn):
    data_dic = payload.dict()
    try:
        operate_user_info = get_user_info_from_token(request)
        role_ids = data_dic.pop("role_ids", [])

        # 确保 role_ids 是一个列表
        if role_ids is None:
            role_ids = []

        with transaction.atomic():  # 使用事务
            new_user = Users.objects.create(**data_dic)
            new_user.creator = operate_user_info.username
            new_user.updater = operate_user_info.username
            new_user.password = make_password("123456")
            new_user.save()

            if role_ids:
                new_user.role.set(role_ids)

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        return standard_response(
            code=400,
            message=f"用户名 {data_dic.get('username')} 已存在",
        )
    return new_user.id


@router.post("/batch_delete_user")
def batch_delete_user(request, payload: UserDeleteIn):
    batch_delete_by_id(Users, payload.ids)
    return


def update_user_details(user, data, updater_username):
    for attr, value in data.items():
        if attr == "role_ids":
            user.role.set(value)
        else:
            setattr(user, attr, value)
    user.updater = updater_username
    user.update_time = datetime.now()


@router.put("/user", response=UserOut)
def update_user(request, payload: UpdateUserIn):
    """
    更新用户
    """
    user = get_object_or_404(Users, id=payload.id)
    operate_user_info = get_user_info_from_token(request)

    try:
        with transaction.atomic():
            update_user_details(user, payload.dict(), operate_user_info.username)
            user.save()

        logger.info(f"用户 {user.username} 更新成功")
        return user

    except IntegrityError as e:
        logger.error(f"IntegrityError: {str(e)}")
        return standard_response(
            code=400,
            message=f"{user.username}不能重复",
        )


@router.post("/update_password")
def update_password(request, data: SetPassword):
    """
    修改密码
    """
    operate_user_info = get_user_info_from_token(request)
    operate_username = operate_user_info.username
    update_username = data.username
    # 如果当前操作用户和要修改的用户是同一个人，则修改密码
    if operate_username == update_username:
        user = get_object_or_404(Users, username=update_username)
        # 更新密码，更新人、更新时间
        user.set_password(data.password)
        user.update_time = datetime.now()
        user.save()
        return standard_response(message="密码修改成功")
    else:
        return standard_response(
            code=403, message="对不起, 只能修改自己的密码", success=False
        )


def get_user_permissions(user: Users):
    roles = user.role.prefetch_related(
        Prefetch("menu", to_attr="role_menus"),
        # Prefetch("menu_button", to_attr="role_menu_buttons"),
    )

    menus = set()
    # buttons = set()

    for role in roles:
        menus.update(role.role_menus)
        # buttons.update(role.role_menu_buttons)

    return menus


@router.get("/user_permissions")
def get_user_permission(request):
    """
    根据用户的token，获取用户所有菜单权限
    """
    user_info = get_user_info_from_token(request)
    logger.info(f"用户 {user_info.username} 开始获取权限")
    menus = get_user_permissions(user_info)
    user_permission_tree = build_menu_tree(menus, False)
    return user_permission_tree
