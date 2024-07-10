from datetime import datetime
from typing import Optional, Dict, List

from django.db import models
from django.db.models import Q
from django.shortcuts import get_object_or_404, get_list_or_404

from utils.log_config import logger
from utils.usual import orjson_dumps
from .usual import get_user_info_from_token


# 这里的 get_object_or_404 中的id是数据库id这个字段
# 如果想用其他字段查，比如用firstname，可以使用get_object_or_404(Employee, first_name=first_name)，让前端传first_name过来就行
def create(request, data, model: models):
    """
    创建新记录的函数。
    参数:
    - request: 请求对象，用于获取用户信息。
    - data: 创建记录的数据，可以是字典或者支持dict()方法的对象。
    - model: Django ORM模型，指定要创建的对象类型。

    返回值:
    - 创建成功的实例对象
    """
    if not isinstance(data, dict):
        # 如果data不是字典类型，则转换为字典
        data = data.dict()
    logger.info(f"模型{model},创建数据：{orjson_dumps(data)}")
    user_info = get_user_info_from_token(request)
    if user_info is not None:
        logger.info(f"创建人：{user_info.username}")
        # 从请求中提取用户信息，并添加到数据中作为创建人、修改者
        data["creator"] = user_info.username
        data["updater"] = user_info.username
    # 使用提供的模型和数据创建新记录
    model_instance = model.objects.create(**data)
    return model_instance


def batch_create(request, data, model: models):
    """
    批量创建模型实例。
    参数:
    - request: HTTP请求对象，用于获取用户信息。
    - data: 一个包含创建数据的列表，每个元素可以是字典或者具有dict方法的对象。
    - model: Django模型类，用于实例化和批量创建。

    返回值:
    - query_set: 批量创建后的模型实例对象。
    """
    user_info = get_user_info_from_token(request)
    data_list = []
    for item in data:
        if not isinstance(item, dict):
            item = item.dict()  # 如果item不是字典，则转换为字典

        # 为每个创建的数据项添加默认的创建人、修改者和所属部门信息
        item["creator"] = user_info.username
        item["updater"] = user_info.username
        data_list.append(model(**item))  # 根据字典内容实例化模型对象并添加到列表中
    model_instance = model.objects.bulk_create(data_list)  # 批量创建模型实例
    return model_instance


def get_by_id(model: models, model_id: int):
    """
    根据提供的ID获得模型的对象实例
    """
    model_instance = get_object_or_404(model, id=model_id)
    return model_instance


def delete_by_id(model: models, model_id: int):
    """
    根据提供的ID和模型删除对象实例。
    参数:
    - id: 要删除的对象的ID。
    - model: 对象所属的模型类。

    返回值:
    - 返回被删除的对象实例
    """
    # 根据ID和模型获取对象实例，如果找不到则返回404错误页面
    model_instance = get_object_or_404(model, id=model_id)
    # 删除对象实例
    model_instance.delete()
    return model_instance


def batch_delete_by_id(model: models, ids: List[int]):
    """
    根据提供的ID列表和模型类批量删除对象实例。
    参数:
    - ids: 要删除的对象的ID列表。
    - model: 对象所属的模型类。

    返回值:
    - 返回被删除的对象实例列表
    """
    # 根据ID列表和模型获取对象实例列表，如果找不到则返回404错误页面
    model_instances = get_list_or_404(model, id__in=ids)
    # 删除对象实例
    [instance.delete() for instance in model_instances]
    return


def soft_delete_by_id(model: models, model_id: int):
    pass


def update_by_id(request, data, model: models, model_id: int):
    """
    更新给定模型实例的数据。

    参数:
    - request: HTTP请求对象，用于获取用户信息。
    - id: 要更新的模型实例的ID。
    - data: 包含更新数据的实例，应能转换为字典格式。
    - model: 要更新的模型类。

    返回值:
    - 更新后的模型实例。
    """
    dict_data = data.dict()  # 将data转换为字典格式
    user_info = get_user_info_from_token(request)  # 从请求中获取用户信息
    if user_info is not None:
        # 为更新的数据添加修改者信息
        dict_data["updater"] = user_info.username
        dict_data["update_time"] = datetime.now()
    model_instance = get_object_or_404(model, id=model_id)  # 获取指定ID的模型实例
    # 遍历字典，将更新的数据设置到模型实例上
    for attr, value in dict_data.items():
        setattr(model_instance, attr, value)
    model_instance.save()  # 保存更新
    return model_instance


def retrieve(
    request, model: models, filters, query_types: Optional[Dict[str, str]] = None
):
    """
    根据提供的过滤条件从数据库中检索模型实例。

    参数:
    - request: HttpRequest对象，用于获取请求信息。
    - model: Django模型类，指定要检索的数据模型。
    - filters: BaseFilter类的实例，包含过滤条件。默认为 BaseFilter()，即无条件过滤。
    - query_types: 每个字段的查询类型，dict，包含字段名称及其查询类型的字典。
        格式：{"field_name": "query_type"}
        contains: 模糊查询
        exact: 精确查询

    返回值:
    - query_set: 一个Django QuerySet对象，包含根据过滤条件检索到的模型实例。
    """
    if filters is not None:
        filter_dict = filters.dict(exclude_none=True)
        # try:
        #     filter_dict.pop("pagination", None)  # 安全地删除 pagination 键
        # except KeyError:
        #     pass
        query_conditions = Q()
        for attr, value in filter_dict.items():
            if query_types and attr in query_types:
                query_type = query_types[attr]
                if query_type == "contains":
                    query_conditions &= Q(**{f"{attr}__icontains": value})
                elif query_type == "exact":
                    query_conditions &= Q(**{attr: value})
                else:
                    raise ValueError(
                        f"不支持的查询类型，只支持contains和exact: {query_type}"
                    )
            else:
                # 默认使用模糊查询
                query_conditions &= Q(**{f"{attr}__icontains": value})
        query_set = model.objects.filter(query_conditions)
    else:
        # 如果没有有效的过滤条件，则返回包含所有模型实例的queryset
        query_set = model.objects.all()

    return query_set
