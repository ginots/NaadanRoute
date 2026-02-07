from django.shortcuts import render

from navigator.models import TableBlog

from navigator.models import TableCategories

from navigator.models import TableSubCategories


# Create your views here.
def blog(request):
    blog_list = TableBlog.objects.filter(status="Active").order_by("-date")[:12]
    return render(request, "blogs/blog.html", {"blog":blog_list})

def blog_single(request, blog_slug):
    data = TableBlog.objects.get(slug=blog_slug)
    blog_list = TableBlog.objects.filter(status=data.status).exclude(slug=blog_slug).order_by("-date")[:3]
    tags = [tag.strip() for tag in data.tag.split(",")]
    cate = TableCategories.objects.filter(status="Active")
    return render(request, "blogs/blog_single.html", {"data":data,"tags":tags,
                                                      "cate":cate,"blog_list":blog_list})

def subcategory_blogs(request, sub_id):
    sub = TableSubCategories.objects.get(id=sub_id)
    blog_list = TableBlog.objects.filter(sub_category=sub,status="Active").order_by("-date")[:9]
    return render(request, "blogs/blog.html", {"blog":blog_list})
