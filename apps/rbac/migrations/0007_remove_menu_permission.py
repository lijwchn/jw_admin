# Generated by Django 4.2.13 on 2024-06-29 10:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("rbac", "0006_alter_menubutton_menu"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="menu",
            name="permission",
        ),
    ]
