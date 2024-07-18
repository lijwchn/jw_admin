from ninja.security import HttpBearer
from django.http import HttpRequest
from utils.log_config import logger
from utils.usual import get_user_info_from_token
from core.common_exception import CommonException


class SuperAdminAuth(HttpBearer):
    def authenticate(self, request: HttpRequest, token: str):
        # 使用你已经定义的函数来获取用户对象
        user = get_user_info_from_token(request)
        if user and user.is_superuser:  # 检查用户是否已认证且为超级管理员
            logger.info(f"{user.username} 访问了管理员接口")
            return user
        raise CommonException(message="非管理员不能操作", status_code=403)
