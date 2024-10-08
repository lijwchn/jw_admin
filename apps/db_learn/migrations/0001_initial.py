# Generated by Django 4.2.13 on 2024-06-27 10:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("tagline", models.TextField()),
            ],
            options={
                "verbose_name": "博客表",
                "db_table": "sys_blog",
            },
        ),
        migrations.CreateModel(
            name="Entry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("headline", models.CharField(max_length=255)),
                ("body_text", models.TextField()),
                ("pub_date", models.DateTimeField(verbose_name="date published")),
                (
                    "blog",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="entries",
                        to="db_learn.blog",
                    ),
                ),
            ],
            options={
                "verbose_name": "博客条目表",
                "db_table": "sys_blog_entry",
            },
        ),
    ]
