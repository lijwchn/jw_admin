from typing import Optional, List

from ninja import Schema, ModelSchema

from .models import Users, Dept, Menu


class MenuIn(Schema):
    title: str
    icon: Optional[str] = ""
    path: str
    is_ext: Optional[bool] = False
    type: int
    status: Optional[bool] = True
    parent_id: Optional[List[int]] = None
    order: int


class MenuUpdateIn(MenuIn):
    id: int


class MenuOut(ModelSchema):
    class Meta:
        model = Menu
        fields = "__all__"


class RoleIn(Schema):
    name: str
    code: str
    status: Optional[bool] = True
    remark: Optional[str] = None


class RoleOut(Schema):
    id: int
    name: str
    code: str
    status: Optional[bool] = True
    remark: Optional[str] = None
    menu: Optional[List[MenuOut]] = None  # 使用嵌套的 MenuOut 模式


class RoleUpdateIn(RoleIn):
    id: int


class DeptIn(Schema):
    name: str
    owner: str
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[bool] = True


class DeptOut(ModelSchema):
    class Meta:
        model = Dept
        fields = "__all__"


class DeptFilterSchema(Schema):
    name: Optional[str] = None
    status: Optional[bool] = None


class CreateUserIn(Schema):
    username: str
    name: str
    email: Optional[str] = None
    mobile: Optional[str] = None
    avatar: Optional[str] = None
    status: Optional[bool] = True
    gender: Optional[int] = 1
    user_type: Optional[int] = 0
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dept_id: Optional[int] = None
    role_ids: Optional[List[int]] = None


class UpdateUserIn(CreateUserIn):
    id: int


class UserDeleteIn(Schema):
    ids: Optional[List[int]] = None


class UserOut(ModelSchema):
    dept: Optional[DeptOut] = None  # 使用嵌套的 DeptOut 模式
    role: Optional[List[RoleOut]] = None  # 使用嵌套的 RoleOut 模式

    class Meta:
        model = Users
        fields = [
            "id",
            "username",
            "name",
            "email",
            "mobile",
            "avatar",
            "status",
            "gender",
            "dept",
            "role",
        ]


class UserFilterSchema(Schema):
    username: Optional[str] = None
    name: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[bool] = None
    dept_id: Optional[int] = None


class SetPassword(Schema):
    username: str
    password: str


class MenuFilterSchema(Schema):
    title: Optional[str] = None
    status: Optional[bool] = None
    types: Optional[List[int]] = None
    include_buttons: Optional[bool] = True


class RoleFilterSchema(Schema):
    name: Optional[str] = None
    code: Optional[str] = None
    status: Optional[bool] = True


class RoleMenuIn(Schema):
    menu_ids: List[int]
    # menu_button_ids: List[int]


class MenuButtonIn(Schema):
    id: Optional[int] = None
    title: str
    parent_id: int
    menu: Optional[int] = None
    type: Optional[int] = 3


# class MenuButtonOut(ModelSchema):
#     class Meta:
#         model = MenuButton
#         fields = "__all__"
class MenuButtonOut(Schema):
    id: int
    title: str
    menu_id: int
    type: int
