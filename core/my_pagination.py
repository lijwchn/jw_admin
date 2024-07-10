from typing import Any, List

from django.core.exceptions import FieldDoesNotExist
from django.db.models import QuerySet
from django.forms.models import model_to_dict
from ninja import Field, Schema
from ninja.pagination import PaginationBase


# model_to_dict 默认不会包含 auto_now 和 auto_now_add 字段
# 自定义 model_to_dict，确保包含所有字段
def model_to_dict_custom(instance, fields=None, exclude=None):
    data = model_to_dict(instance, fields=fields, exclude=exclude)
    for field in ["create_time", "update_time"]:
        try:
            field_value = getattr(instance, field, None)
            if field_value:
                data[field] = field_value
        except FieldDoesNotExist:
            continue
    return data


# 自定义分页类
class MyPagination(PaginationBase):
    # 自定义分页所需的参数
    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: int = Field(10, gt=-1)

    # InputSource = Body(...)

    class Output(Schema):
        items: List[Any]
        count: int
        total_page: int

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        """
        分页查询
        :param queryset: 查询集
        :param pagination: 分页识别参数
        :param params: 其他参数
        :return: 分页后的query_set
        """
        offset = (pagination.page - 1) * pagination.page_size
        paginated_queryset = queryset[offset : offset + pagination.page_size]

        # # 将 QuerySet 对象转换为字典数据
        # items = [model_to_dict_custom(item) for item in paginated_queryset]
        # 获取总数和总页数
        count = queryset.count()
        total_page = (count + pagination.page_size - 1) // pagination.page_size

        return {"items": paginated_queryset, "count": count, "total_page": total_page}
