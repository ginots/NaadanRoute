from django.urls import path
from . import views

urlpatterns = [
    path("tours_dashboard/", views.tours_dashboard, name="tours_dashboard"),
    path("tours_details/<package_slug>/", views.tours_details, name="tours_details" ),
    path("book_now/<package_slug>/", views.book_now, name="book_now"),
    path("save_booking/<int:tour_id>/", views.save_booking, name="save_booking"),
    path("ai_chat/", views.ai_chat, name="ai_chat"),
]