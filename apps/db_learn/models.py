from django.db import models


# 了解 ForeignKey 用法
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    class Meta:
        db_table = "sys_blog"
        verbose_name = "博客表"


class Entry(models.Model):
    blog = models.ForeignKey(
        Blog, on_delete=models.SET_NULL, related_name="entries", null=True, blank=True
    )
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateTimeField("date published")

    class Meta:
        db_table = "sys_blog_entry"
        verbose_name = "博客条目表"
