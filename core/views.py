from django.db.models import Count
from django.shortcuts import render,redirect

from navigator.models import TableTravelPackages
from tours.models import TableChatMessages

from navigator.models import TableBlog


# Create your views here.
def index(request):
    pac = TableTravelPackages.objects.filter(status="Active").prefetch_related("media")[:9]
    wish_pac = TableTravelPackages.objects.filter(status="Active") \
        .prefetch_related("media") \
        .annotate(wish_count=Count("wishlisted_package")) \
        .order_by("-wish_count")[:5]
    blog = TableBlog.objects.filter(status="Active").order_by("-date")[:3]
    session_key = request.session.session_key
    chat_history = []
    if session_key:
        chat_history = TableChatMessages.objects.filter(session_id=session_key).order_by("timestamp")
    return render(request,"core/index.html",{"pac":pac,"chat_history":chat_history,
                                             "wish_pac":wish_pac,"blog":blog})

