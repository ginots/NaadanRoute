from datetime import timezone
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.db.models import Sum
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from .models import *
from tours.models import TableAddress,TableTourPurchased
from navigator.models import TableTravelPackages


# Create your views here.


def save_signup(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if len(name) < 3 or len(name) > 15:
            messages.error(request, "Username must be between 3 and 15 characters.")
            return redirect("/")

        if User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect("/")

        if len(password) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("/")

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        messages.success(request, "Signup successful! Please sign in.")
        return redirect("/")
    messages.error(request, "Invalid Request")
    return redirect("/")

def check_signin(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}")
            return redirect("/")
        else:
            messages.error(request, "Invalid email or password.")
            return redirect("/")
    messages.error(request, "Invalid Request")
    return redirect("/")

def sign_out(request):
    logout(request)
    messages.success(request, "Logout successful")
    return redirect("/")

@login_required
def profile(request):
    user = request.user
    user_address = TableAddress.objects.filter(user=user)
    bookings = TableTourPurchased.objects.filter(user=user).order_by("-id")
    booking_count = TableTourPurchased.objects.filter(user=user,order_status="Completed").count()
    wishlist = TableWishlist.objects.filter(user=user).order_by("-id")[:3]
    wishlist_count = TableWishlist.objects.filter(user=user).count()
    spending = sum(i.price for i in bookings.filter(order_status="Completed"))

    current_year = timezone.now().year
    previous_year = current_year - 1

    spending_this_year = bookings.filter(order_status="Completed",invoice_date__year=current_year).aggregate(
        total=Sum("price"))["total"] or 0
    spending_last_year = bookings.filter(order_status="Completed",invoice_date__year=previous_year).aggregate(
        total=Sum("price"))["total"] or 0
    spending_diff = spending_this_year - spending_last_year

    return render(request,"accounts/profile.html",{"user":user,
                                               "user_address":user_address,"bookings":bookings,
                                               "booking_count":booking_count,"wishlist":wishlist,
                                               "wishlist_count":wishlist_count,"spending":spending,
                                                   "spending_diff":spending_diff})

@login_required
def save_first_address(request):
    if request.method == "POST":
        tab_obj = TableAddress()
        tab_obj.user = request.user
        tab_obj.fullname = request.POST.get("fullname")
        tab_obj.email = request.POST.get("email")
        tab_obj.phone = request.POST.get("phone")
        tab_obj.address = request.POST.get("address")
        tab_obj.city = request.POST.get("city")
        tab_obj.district = request.POST.get("district")
        tab_obj.state = request.POST.get("state")
        tab_obj.postcode = request.POST.get("postcode")
        tab_obj.save()
        return redirect("profile")
    messages.error(request, "Invalid Request")
    return redirect("profile")

def wishlist_toggle(request):
    if request.method == "POST":
        package_id = request.POST.get("package_id")
        action = request.POST.get("action")
        package = get_object_or_404(TableTravelPackages, id=package_id)

        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Not logged in"}, status=403)

        if action == "add":
            TableWishlist.objects.get_or_create(user=request.user, package=package)
        else:
            TableWishlist.objects.filter(user=request.user, package=package).delete()

        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error"})

@login_required
def view_all_wishlists(request):
    wishlist_items = TableWishlist.objects.filter(user=request.user).select_related("package")
    return render(request,"accounts/view_all_wishlists.html",{"wishlist_items":wishlist_items,})

@login_required
def remove_from_wishlist(request, wishlist_id):
    if request.method == 'POST':
        item = get_object_or_404(TableWishlist, id=wishlist_id, user=request.user)
        item.delete()
        messages.success(request, "Removed from your wishlist.")
    return redirect("view_all_wishlists")

@login_required
def change_password(request):
    if request.method == 'POST':
        old_pass = request.POST.get('old_password')
        new_pass = request.POST.get('new_password')
        confirm_pass = request.POST.get('confirm_password')
        user = request.user

        if not check_password(old_pass, user.password):
            messages.error(request, "Current password is incorrect.")
            return redirect("profile")

        if new_pass != confirm_pass:
            messages.error(request, "New passwords do not match.")
            return redirect("profile")

        if len(new_pass) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return redirect("profile")

        user.set_password(new_pass)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, "Password successfully updated!")
        return redirect("profile")
    messages.error(request, "Invalid Request")
    return redirect("profile")