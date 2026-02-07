from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from . import views

superuser_only = user_passes_test(lambda u: u.is_superuser)
urlpatterns = [
    path("navigator_login/", views.navigator_login, name="navigator_login"),
    path("admin_check/", views.admin_check, name="admin_check"),
    path("dashboard/", staff_member_required(views.dashboard), name="dashboard"),
    path("categories/", staff_member_required(views.categories), name="categories"),
    path("add_categories/", superuser_only(views.add_categories), name="add_categories"),
    path("save_categories/", superuser_only(views.save_categories), name="save_categories"),
    path("edit_categories/<int:cate_id>/", superuser_only(views.edit_categories), name="edit_categories"),
    path("update_categories/<int:cate_id>/", superuser_only(views.update_categories), name="update_categories"),
    path("delete_categories/<int:cate_id>/", superuser_only(views.delete_categories), name="delete_categories"),
    path("sub_categories/", staff_member_required(views.sub_categories), name="sub_categories"),
    path("add_sub_categories/", superuser_only(views.add_sub_categories), name="add_sub_categories"),
    path("save_sub_categories/", superuser_only(views.save_sub_categories), name="save_sub_categories"),
    path("edit_sub_categories/<int:sub_id>/", superuser_only(views.edit_sub_categories), name="edit_sub_categories"),
    path("update_sub_categories/<int:sub_id>/", superuser_only(views.update_sub_categories), name="update_sub_categories"),
    path("delete_sub_categories/<int:sub_id>/", superuser_only(views.delete_sub_categories), name="delete_sub_categories"),
    path("blogs/", staff_member_required(views.blogs), name="blogs"),
    path("add_blogs/", superuser_only(views.add_blogs), name="add_blogs"),
    path("save_blog/", superuser_only(views.save_blog), name="save_blog"),
    path("edit_blogs/<int:blog_id>/", superuser_only(views.edit_blogs), name="edit_blogs"),
    path("update_blog/<int:blog_id>/", superuser_only(views.update_blog), name="update_blog"),
    path("delete_blogs/<int:blog_id>/", superuser_only(views.delete_blogs), name="delete_blogs"),
    path("travel_packages/", staff_member_required(views.travel_packages), name="travel_packages"),
    path("add_travel_packages/", superuser_only(views.add_travel_packages), name="add_travel_packages"),
    path("save_travel_packages/", superuser_only(views.save_travel_packages), name="save_travel_packages"),
    path("edit_travel_packages/<int:pac_id>/", superuser_only(views.edit_travel_packages), name="edit_travel_packages"),
    path("update_travel_packages/<int:pac_id>/", superuser_only(views.update_travel_packages), name="update_travel_packages"),
    path("delete_package_image/<int:img_id>/", superuser_only(views.delete_package_image), name="delete_package_image"),
    path("delete_travel_packages/<int:pac_id>/", superuser_only(views.delete_travel_packages), name="delete_travel_packages"),
    path("orders/", staff_member_required(views.orders), name="orders"),
    path("delete_order/<int:order_id>/", superuser_only(views.delete_order), name="delete_order"),
    path("invoice/<int:order_id>", staff_member_required(views.invoice), name="invoice"),
    path("change_order_status/<int:order_id>", staff_member_required(views.change_order_status), name="change_order_status"),
    path("view_all_orders/", staff_member_required(views.view_all_orders), name="view_all_orders"),
    path("export_orders_csv/", staff_member_required(views.export_orders_csv), name="export_orders_csv"),

]