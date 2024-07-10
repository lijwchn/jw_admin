from django.db import models


# 定义数据库常用字段
class CoreModel(models.Model):
    """核心默认基础类"""

    creator = models.CharField(
        max_length=255, null=True, blank=True, help_text="创建人", default="system"
    )
    updater = models.CharField(
        max_length=255, null=True, blank=True, help_text="修改人", default="system"
    )
    update_time = models.DateTimeField(
        auto_now=True, help_text="修改时间", verbose_name="修改时间"
    )
    create_time = models.DateTimeField(
        auto_now_add=True, help_text="创建时间", verbose_name="创建时间"
    )

    class Meta:
        abstract = True


class CoreModelSoftDelete(CoreModel):
    is_deleted = models.CharField(default=0, help_text="是否删除", max_length=36)

    class Meta:
        abstract = True
