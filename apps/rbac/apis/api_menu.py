from django.db.models import Prefetch, Q
from ninja import Router

from apps.rbac.models import Menu, MenuButton
from apps.rbac.schemas import MenuOut, MenuIn, MenuFilterSchema, MenuUpdateIn
from core.standard_response import standard_response
from utils.base_curd import create, get_by_id, delete_by_id, update_by_id
from utils.usual import build_menu_tree

router = Router()


@router.get("/menu/{menu_id}", response=MenuOut)
def get_user_by_id(request, menu_id: int):
    data = get_by_id(Menu, menu_id)
    return data


@router.post("/menu_list")
def list_menu(request, filter: MenuFilterSchema):
    """
    返回所有菜单的树形结构的列表，用于前端给角色分配权限时使用
    """
    # 如果有查询条件，则根据条件查询
    filter_dict = filter.dict(exclude_none=True)
    include_buttons = filter_dict.pop("include_buttons", True)
    if filter is not None:
        query_conditions = Q()
        for key, value in filter_dict.items():
            if key == "title":
                query_conditions.add(Q(title__icontains=value), Q.AND)
            if key == "status":
                query_conditions.add(Q(status=value), Q.AND)
            if key == "types":
                query_conditions.add(Q(type__in=value), Q.AND)
        query_set = Menu.objects.filter(query_conditions)
    else:
        query_set = Menu.objects.all()

    menus = query_set.prefetch_related(
        Prefetch("menu_buttons", queryset=MenuButton.objects.all())
    ).order_by("order")

    menu_tree = build_menu_tree(menus, include_buttons)
    return menu_tree


def check_menu_type(parent_id, menu_type):
    """
    1、父级菜单没选，menu_type 只能等于 1
    2、父级菜单选了 1 个，type只能等于 2
    3、父级菜单选了 2 个，不成立，直接失败
    """
    if parent_id is None:
        if menu_type != 1:
            return False
        else:
            return True
    if len(parent_id) == 1:
        if menu_type != 2:
            return False
    if len(parent_id) == 2:
        return False
    return True


@router.post("/menu")
def create_menu(request, payload: MenuIn):
    """
    新增菜单
    """

    # 如果前端传了 [] 空列表，说明没有选择父级菜单，则将parent_id置为None
    if is_empty_list(payload.parent_id):
        payload.parent_id = None

    result = check_menu_type(payload.parent_id, payload.type)
    if not result:
        return standard_response(
            code=400, message="菜单类型错误，请严格匹配菜单层级关系", success=False
        )
    else:
        # 为了兼容前端的传过来的parent_id列表，将parent_id的最后一个元素取出来
        if payload.parent_id is not None:
            payload.parent_id = payload.parent_id[-1]

        menu = create(request, payload, Menu)
        return menu.id


def is_empty_list(obj):
    """
    判断对象是否为空列表
    """
    # 首先检查obj是否是list类型
    if isinstance(obj, list):
        # 然后检查这个list是否为空
        return len(obj) == 0
    else:
        return False


@router.put("/menu")
def update_menu(request, payload: MenuUpdateIn):
    """
    更新菜单
    """
    menu_id = payload.id

    # 如果前端传了 [] 空列表，说明没有选择父级菜单，则将parent_id置为None
    if is_empty_list(payload.parent_id):
        payload.parent_id = None

    result = check_menu_type(payload.parent_id, payload.type)
    if not result:
        return standard_response(
            code=400, message="菜单类型错误，请严格匹配菜单层级关系", success=False
        )

    # 为了兼容前端的菜单树，将parent_id的第一个元素取出来
    if payload.parent_id is not None:
        payload.parent_id = payload.parent_id[0]
    # 如果是二级菜单，则icon字段置为空
    if payload.type == 2:
        payload.icon = ""

    data = update_by_id(request, payload, Menu, menu_id)
    return data.id


@router.delete("/menu/{menu_id}")
def delete_menu(request, menu_id: int):
    """
    删除菜单后，会将 system_menu_button/system_role_menu 中关联的数据一并删除
    """
    data = delete_by_id(Menu, menu_id)
    return data.id
