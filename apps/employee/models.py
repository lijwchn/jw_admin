from django.db import models

from core.base_model import CoreModelSoftDelete


class Department(CoreModelSoftDelete):
    title = models.CharField(max_length=100)

    class Meta:
        db_table = "sys_department"
        verbose_name = "部门表"


class Employee(CoreModelSoftDelete):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department, on_delete=models.DO_NOTHING, db_constraint=False
    )
    birthdate = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "sys_employee"
        verbose_name = "员工表"
