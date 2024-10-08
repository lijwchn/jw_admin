# Generated by Django 4.2.13 on 2024-06-30 02:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rbac", "0011_alter_menu_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="menu",
            name="parent",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="children",
                to="rbac.menu",
                verbose_name="上级菜单",
            ),
        ),
        migrations.AlterField(
            model_name="menubutton",
            name="menu",
            field=models.ForeignKey(
                db_constraint=False,
                help_text="关联菜单",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="menu_buttons",
                to="rbac.menu",
                verbose_name="关联菜单",
            ),
        ),
    ]
