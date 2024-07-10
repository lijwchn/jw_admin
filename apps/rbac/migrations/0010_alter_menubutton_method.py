# Generated by Django 4.2.13 on 2024-06-30 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rbac", "0009_role_remark_alter_users_groups_alter_users_is_active_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menubutton",
            name="method",
            field=models.IntegerField(
                blank=True,
                choices=[
                    (0, "GET"),
                    (1, "POST"),
                    (2, "PUT"),
                    (3, "DELETE"),
                    (4, "PATCH"),
                    (5, "HEAD"),
                    (6, "OPTIONS"),
                ],
                default=0,
                help_text="接口请求方法",
                null=True,
                verbose_name="接口请求方法",
            ),
        ),
    ]
