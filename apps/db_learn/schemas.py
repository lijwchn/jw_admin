from ninja import Schema, ModelSchema
from .models import Blog


class BlogOut(ModelSchema):
    class Meta:
        model = Blog
        fields = "__all__"
