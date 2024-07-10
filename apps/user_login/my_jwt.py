from django.contrib.auth import authenticate
from ninja.router import Router
from ninja_jwt.tokens import RefreshToken

from core.standard_response import standard_response
from .schamas import UserLoginSchema

router = Router()


@router.post("/login")
def user_login(request, user_login_schema: UserLoginSchema):
    authenticated_user = authenticate(**user_login_schema.dict())
    # 如果 authenticate 函数返回 None,则说明用户名或密码错误
    if not authenticated_user:
        return standard_response(
            code=401, message="用户名或密码错误，或者用户未激活", success=False
        )
    user_info = {
        "id": authenticated_user.id,
        "username": authenticated_user.username,
        "email": authenticated_user.email,
    }
    # 如果用户名或密码正确,则返回 token
    refresh_token = RefreshToken.for_user(authenticated_user)
    return standard_response(
        data={
            "refresh": str(refresh_token),
            "access": str(refresh_token.access_token),
            "user_info": user_info,
        }
    )
