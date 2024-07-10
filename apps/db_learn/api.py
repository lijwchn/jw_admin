from ninja import Router
from django.shortcuts import get_object_or_404
from .models import Blog, Entry
from .schemas import BlogOut
from core.standard_response import standard_response

router = Router()


@router.get("/blog/{blog_id}")
def get_blog_by_id(request, blog_id: int):
    blogs = get_object_or_404(Blog, id=blog_id)
    # entry = get_object_or_404(Entry, id=blog_id)
    return standard_response(data=blogs)
