from django.urls import path
from . import views

urlpatterns = [

    path("save_signup/", views.save_signup, name="save_signup"),
    path("check_signin/", views.check_signin, name="check_signin"),
    path("sign_out/", views.sign_out, name="sign_out"),
    path("profile/", views.profile, name="profile"),
    path("save_first_address/", views.save_first_address, name="save_first_address"),
    path("wishlist_toggle/", views.wishlist_toggle, name="wishlist_toggle"),
    path("view_all_wishlists/", views.view_all_wishlists, name="view_all_wishlists"),
    path("remove_from_wishlist/<int:wishlist_id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("change_password/", views.change_password, name="change_password"),
]