from django.contrib.auth.models import AbstractUser
from django.db import models

from core.base_model import CoreModel, CoreModelSoftDelete


# db_constraint=False 指示Django在数据库层面不要为字段创建外键约束，但是在orm模型层中，Django会自动创建外键约束。
class Users(AbstractUser, CoreModel):
    GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),
    )
    USER_TYPE = (
        (0, "后台用户"),
        (1, "前台用户"),
    )
    username = models.CharField(
        max_length=50, unique=True, db_index=True, verbose_name="用户账号"
    )
    email = models.EmailField(
        max_length=255, verbose_name="邮箱", null=True, blank=True, help_text="邮箱"
    )
    mobile = models.CharField(
        max_length=50, verbose_name="电话", null=True, blank=True, help_text="电话"
    )
    avatar = models.TextField(
        verbose_name="头像", null=True, blank=True, help_text="头像"
    )
    name = models.CharField(max_length=40, verbose_name="姓名", help_text="姓名")
    status = models.BooleanField(default=True, verbose_name="状态", help_text="状态")
    gender = models.IntegerField(
        choices=GENDER_CHOICES, default=1, verbose_name="性别", null=True, blank=True
    )
    user_type = models.IntegerField(
        choices=USER_TYPE, default=0, verbose_name="用户类型", null=True, blank=True
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    role = models.ManyToManyField(
        to="Role", verbose_name="关联角色", db_constraint=False, help_text="关联角色"
    )
    dept = models.ForeignKey(
        to="Dept",
        verbose_name="所属部门",
        on_delete=models.SET_NULL,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联部门",
    )

    class Meta:
        db_table = "system_users"
        verbose_name = "用户表"


class Role(CoreModel):
    name = models.CharField(
        max_length=64, verbose_name="角色名称", help_text="角色名称"
    )
    code = models.CharField(
        max_length=64, unique=True, verbose_name="角色编码", help_text="角色编码"
    )
    status = models.BooleanField(
        default=True, verbose_name="角色状态", help_text="角色状态"
    )
    menu = models.ManyToManyField(
        to="Menu", verbose_name="关联菜单", db_constraint=False, help_text="关联菜单"
    )
    menu_button = models.ManyToManyField(
        to="MenuButton", verbose_name="关联菜单的接口按钮", db_constraint=False
    )
    remark = models.CharField(
        max_length=50, verbose_name="备注", null=True, blank=True, help_text="备注"
    )

    class Meta:
        db_table = "system_role"
        verbose_name = "角色表"
        verbose_name_plural = verbose_name


class Menu(CoreModel):
    ISLINK_CHOICES = (
        (0, "否"),
        (1, "是"),
    )
    parent = models.ForeignKey(
        to="Menu",  # 或者写做 "self"
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="上级菜单",
        null=True,
        blank=True,
        db_constraint=False,
    )
    icon = models.CharField(
        max_length=64,
        default="",
        verbose_name="菜单图标",
        null=True,
        blank=True,
    )
    title = models.CharField(
        max_length=64, verbose_name="菜单名称", help_text="菜单名称"
    )
    is_ext = models.BooleanField(
        default=False, verbose_name="是否外链", help_text="是否外链"
    )
    type = models.IntegerField(verbose_name="菜单等级，一级二级等", default=1)
    path = models.CharField(
        max_length=128,
        verbose_name="路由地址",
        null=True,
        blank=True,
        help_text="路由地址",
    )
    status = models.BooleanField(
        default=True, blank=True, verbose_name="菜单状态", help_text="菜单状态"
    )
    order = models.IntegerField(
        default=1, verbose_name="排序", help_text="排序", null=True, blank=True
    )

    class Meta:
        db_table = "system_menu"
        verbose_name = "菜单表"
        verbose_name_plural = verbose_name


class MenuButton(CoreModel):
    METHOD_CHOICES = (
        (0, "GET"),
        (1, "POST"),
        (2, "PUT"),
        (3, "DELETE"),
        (4, "PATCH"),
        (5, "HEAD"),
        (6, "OPTIONS"),
    )
    menu = models.ForeignKey(
        to="Menu",
        db_constraint=False,
        related_name="menu_buttons",
        on_delete=models.CASCADE,
        verbose_name="关联菜单",
        help_text="关联菜单",
    )
    title = models.CharField(max_length=64, verbose_name="名称", help_text="名称")
    type = models.IntegerField(verbose_name="菜单等级，3是按钮", default=3)
    code = models.CharField(max_length=64, verbose_name="权限值", help_text="权限值")
    api = models.CharField(
        max_length=200, verbose_name="接口地址", help_text="接口地址"
    )
    method = models.IntegerField(
        choices=METHOD_CHOICES,
        default=0,
        verbose_name="接口请求方法",
        null=True,
        blank=True,
        help_text="接口请求方法",
    )
    status = models.BooleanField(
        default=True, blank=True, verbose_name="按钮状态", help_text="按钮状态"
    )

    class Meta:
        db_table = "system_menu_button"
        verbose_name = "菜单按钮权限表"
        verbose_name_plural = verbose_name


class Dept(CoreModel):
    name = models.CharField(
        max_length=64, verbose_name="部门名称", help_text="部门名称"
    )
    owner = models.CharField(
        max_length=32, verbose_name="负责人", null=True, blank=True, help_text="负责人"
    )
    phone = models.CharField(
        max_length=32,
        verbose_name="联系电话",
        null=True,
        blank=True,
        help_text="联系电话",
    )
    email = models.EmailField(
        max_length=32, verbose_name="邮箱", null=True, blank=True, help_text="邮箱"
    )
    status = models.BooleanField(
        default=True,
        verbose_name="部门状态",
        null=True,
        blank=True,
        help_text="部门状态",
    )

    class Meta:
        db_table = "system_dept"
        verbose_name = "部门表"
        verbose_name_plural = verbose_name
