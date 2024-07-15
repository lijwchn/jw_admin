from typing import Any, Optional

from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI
from ninja.renderers import JSONRenderer

from core.standard_response import format_datetime_in_dict
from utils.log_config import logger


class MyJSONRenderer(JSONRenderer):
    json_dumps_params = {"ensure_ascii": False}


class MyNinjaAPI(NinjaAPI):
    """
    继承 NinjaAP，重写里面的create_response方法，大部分都是源码
    解决了两个问题
    1、通过修改std_data格式，返回一个标准的响应
    2、设置 MyJSONRenderer 中的json_dumps_params为{"ensure_ascii": False}，解决响应中如果有中文，返回unicode的问题
    当在接口中直接返回对象时，可以被这个create_response方法捕获返回标准数据
    """
    def __init__(self):
        super().__init__()
        self.renderer = MyJSONRenderer()

    def create_response(
        self,
        request: HttpRequest,
        data: Any,
        *,
        status: Optional[int] = None,
        temporal_response: HttpResponse = None,
    ) -> HttpResponse:
        if temporal_response:
            status = temporal_response.status_code
        assert status

        # 修改标准输出格式，其他都是源码
        std_data = {"code": 200, "data": data, "message": "操作成功", "success": True}
        content = self.renderer.render(
            request,
            data=format_datetime_in_dict(std_data),
            response_status=status,
        )
        if temporal_response:
            response = temporal_response
            response.content = content
        else:
            response = HttpResponse(
                content,
                status=status,
                content_type=self.get_content_type(),
            )

        logger.info(f"由 my_ninja 创建的响应")
        return response
