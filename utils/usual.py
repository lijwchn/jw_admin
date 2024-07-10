import orjson
from django.http import HttpRequest
from ninja_jwt.authentication import JWTBaseAuthentication
from ninja_jwt.exceptions import AuthenticationFailed, InvalidToken

from utils.log_config import logger


# 从token中获取用户信息
def get_user_info_from_token(request: HttpRequest):
    jwt_auth = JWTBaseAuthentication()

    # 从请求头中提取 JWT 令牌
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logger.error("授权标头丢失或格式不正确")
        return None

    token = auth_header.split(" ")[1]

    try:
        user = jwt_auth.jwt_authenticate(request, token)
        return user
    except (InvalidToken, AuthenticationFailed) as e:
        # 处理无效令牌或认证失败的情况
        logger.error(f"认证失败: {str(e)}")
        return None


def orjson_dumps(data):
    return orjson.dumps(data).decode("utf-8")


def build_menu_tree(
        menus,
        include_buttons: bool,
        parent_id=None,
):
    """
    构建菜单树形结构
    """
    tree = []
    for menu in menus:
        if menu.parent_id == parent_id:
            # 创建菜单字典
            menu_dict = {
                # "random_id": str(uuid.uuid4()),
                "id": menu.id,
                "title": menu.title,
                "icon": menu.icon,
                "path": menu.path,
                "type": menu.type,
                "order": menu.order,
                "status": menu.status,
                "is_ext": menu.is_ext,
                "children": [],
            }

            # 递归构建子菜单
            children = build_menu_tree(
                menus,
                include_buttons,
                menu.id,
            )
            if children:
                for child in children:
                    if not child["children"]:  # 如果子菜单没有子菜单（即是二级菜单）
                        if include_buttons:
                            child["children"] = [
                                {
                                    # "random_id": str(uuid.uuid4()),
                                    "id": btn.id,
                                    "title": btn.title,
                                    "code": btn.code,
                                    "api": btn.api,
                                    "method": btn.method,
                                    "type": btn.type,
                                    "status": btn.status,
                                }
                                for btn in menu.menu_buttons.all()
                            ]
                    menu_dict["children"].append(child)
            else:
                # 如果没有子菜单，并且menu_buttons属于这个菜单（即是二级菜单）
                if include_buttons:
                    menu_dict["children"] = [
                        {
                            # "random_id": str(uuid.uuid4()),
                            "id": btn.id,
                            "title": btn.title,
                            "code": btn.code,
                            "api": btn.api,
                            "method": btn.method,
                            "type": btn.type,
                            "status": btn.status,
                        }
                        for btn in menu.menu_buttons.all()
                    ]

            tree.append(menu_dict)

    tree.sort(key=lambda x: x["order"])
    return tree

# def build_user_menu_tree(menus, buttons):
#     """
#     根据用户构建菜单树列表
#     """
#     menu_dict = {menu.id: menu for menu in menus}
#     tree = []
#     button_dict = {}
#
#     # 构建菜单的树形结构
#     for menu in menus:
#         if menu.parent_id:
#             parent = menu_dict.get(menu.parent_id)
#             if parent:
#                 if hasattr(parent, "children") and parent.children.name is None:
#                     parent.children = []
#                 parent.children.append(menu)
#         else:
#             tree.append(menu)
#
#         # 关联按钮
#         button_dict[menu.id] = [
#             button for button in buttons if button.menu_id == menu.id
#         ]
#
#     # 递归附加子菜单和按钮
#     def attach_buttons(menu):
#         menu_buttons = button_dict.get(menu.id, [])
#         menu.menu_buttons = menu_buttons
#         if hasattr(menu, "children"):
#             for child in menu.children:
#                 attach_buttons(child)
#
#     for root_menu in tree:
#         attach_buttons(root_menu)
#
#     return tree
