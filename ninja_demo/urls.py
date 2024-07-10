from django.contrib import admin
from django.urls import path
from ninja_jwt.authentication import JWTAuth

from apps.employee.api import router as employee_router
from apps.manege_mock.api import router as mock_router
from apps.rbac.apis.api_dept import router as system_dept
from apps.rbac.apis.api_menu import router as system_menu
from apps.rbac.apis.api_menu_button import router as system_menu_button
from apps.rbac.apis.api_role import router as system_role
from apps.rbac.apis.api_user import router as system_user
from apps.user_login.my_jwt import router as login_router
from core.my_ninja import MyNinjaAPI

api = MyNinjaAPI()

# api.add_router("/employee", employee_router, tags=["员工增删改查"], auth=JWTAuth())
api.add_router("/employee", employee_router, tags=["员工增删改查"])
api.add_router("/auth", login_router, tags=["用户登录获取token"])
api.add_router("/mock", mock_router, tags=["前端mock的数据"])
# api.add_router("/learn", db_learn_router, tags=["学习"])
api.add_router("/system", system_user, tags=["rbac用户管理"], auth=JWTAuth())
api.add_router("/system", system_dept, tags=["部门管理"], auth=JWTAuth())
api.add_router("/system", system_menu, tags=["rbac菜单管理"], auth=JWTAuth())
api.add_router("/system", system_role, tags=["rbac角色管理"], auth=JWTAuth())
api.add_router("/system", system_menu_button, tags=["rbac菜单按钮管理"], auth=JWTAuth())

from core.exception_handler import not_found_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    # 匹配到所有未找到的路由
    path("api/<path:path>", not_found_view),
]
