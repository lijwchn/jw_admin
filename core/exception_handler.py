import re
import traceback

from django.db import IntegrityError
from django.http import Http404
from ninja.errors import ValidationError

from core.standard_response import standard_response
from core.common_exception import CommonException
from ninja_demo.urls import api
from utils.log_config import logger


# 全局异常函数
@api.exception_handler(Exception)
def all_exception_handler(request, exc: Exception):
    err_msg = str(exc) if exc.args else "系统异常"
    logger.error("Error--> 被全局异常捕获")
    logger.error(traceback.format_exc())
    return standard_response(code=500, message=err_msg, success=False, status=500)


@api.exception_handler(CommonException)
def common_exception_handler(request, exc: CommonException):
    logger.error("Error--> 被通用异常捕获")
    logger.error(traceback.format_exc())
    return standard_response(
        code=exc.code, message=exc.message, success=exc.success, status=exc.status_code
    )


# 访问不存在的资源
@api.exception_handler(Http404)
def not_found_handler(request, exc):
    logger.error("Error--> 访问不存在的资源")
    logger.error(traceback.format_exc())
    return standard_response(message=exc.args[0], success=False, status=404)


# 自定义校验出错时的返回
@api.exception_handler(ValidationError)
def custom_validation_handler(request, exc):
    logger.error("Error--> ValidationError 字段校验出错")
    logger.error(traceback.format_exc())
    errors = exc.errors
    error_messages = []
    for error in errors:
        error_type = error.get("type")
        error_location = error.get("loc")
        error_message = error.get("msg")

        if error_type == "missing" and error_message == "Field required":
            field_name = error_location[-1]
            error_messages.append(f"【{field_name}】不能为空")
        else:
            error_messages.append(
                f"【{error_type}】【{error_location[-1]}】【{error_message}】"
            )

    return standard_response(message="; ".join(error_messages), success=False, code=400)


@api.exception_handler(IntegrityError)
def integrity_error_handler(request, exc):
    logger.error(f"Integrity Error in {request.path}: {traceback.format_exc()}")

    error_code = exc.args[0]
    error_msg = exc.args[1]

    if error_code == 1062 and "Duplicate entry" in error_msg:
        extracted_key = extract_duplicate_key(error_msg)
        return standard_response(message=f"字段{extracted_key}不能重复", success=False)
    else:
        # 更具体的错误处理可以根据需要添加
        return standard_response(message=f"{error_msg}", success=False)


def extract_duplicate_key(error_message):
    """从错误信息中提取重复的键名"""
    match = re.search(r"for key '([^']*)'", error_message)
    return match.group(1) if match else "未知字段"


# 设置全局404处理视图
def not_found_view(request, *args, **kwargs):
    logger.error(traceback.format_exc())
    return standard_response(
        message=f"path:{kwargs.get('path', None)}", success=False, status=404
    )
