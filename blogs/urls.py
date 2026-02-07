from django.urls import path
from . import views

urlpatterns = [
    path("blog/", views.blog, name="blog"),
    path("blog-single/<blog_slug>/", views.blog_single, name="blog-single"),
    path("subcategory-blogs/<int:sub_id>/", views.subcategory_blogs, name="subcategory_blogs"),
]