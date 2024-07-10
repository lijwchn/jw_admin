from datetime import datetime
from typing import Any

from django.db.models import Model
from ninja import Schema
from ninja.responses import Response

from core.my_pagination import model_to_dict_custom


class StandardResponse(Schema):
    code: int
    data: Any = None
    message: str
    success: bool


# 将 datetime 类型字段的格式从 ISO 8601 格式修改为 %Y-%m-%d %H:%M:%S 格式
def format_datetime_in_dict(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(value, list):
                data[key] = [format_datetime_in_dict(item) for item in value]
            elif isinstance(value, dict):
                data[key] = format_datetime_in_dict(value)
    elif isinstance(data, list):
        data = [format_datetime_in_dict(item) for item in data]
    return data


def standard_response(
    code: int = 200,
    data: Any = None,
    message: str = "操作成功",
    success: bool = True,
    status: int = 200,
    **kwargs,
) -> Response:
    """
    标准输出函数
    """
    if data is not None:
        # 如果是 Model 对象，则转换为字典
        if isinstance(data, Model):
            data = model_to_dict_custom(data)
        data = format_datetime_in_dict(data)

    response = StandardResponse(
        code=code,
        data=data if data is not None else [],
        message=message,
        success=success,
    )
    # json_dumps_params={"ensure_ascii": False} 避免非ascii字符乱码，比如中文
    return Response(
        response, status=status, json_dumps_params={"ensure_ascii": False}, **kwargs
    )



