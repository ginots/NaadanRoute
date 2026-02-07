import csv
import datetime

from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Count, Sum
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone

from .models import *
from tours.models import *
from django.contrib.auth.models import User



# Create your views here.

def navigator_login(request):
    return render(request, "navigator/navigator_login.html")

def admin_check(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("/")
    messages.error(request, "Invalid Request")
    return redirect("/")


def dashboard(request):
    now = timezone.now()
    data = TableTourPurchased.objects.filter(invoice_date__year=now.year, invoice_date__month=now.month)
    stats = data.aggregate(
        total_orders=Count("id"),
        total_sales=Sum("price"),
    )
    total_orders = stats["total_orders"] or 0
    total_sales = stats["total_sales"] or 0
    monthly_active_users = User.objects.filter(
        last_login__year=now.year,
        last_login__month=now.month
    ).count()
    new_clients_count = User.objects.filter(
        date_joined__year=now.year,
        date_joined__month=now.month
    ).count()
    return render(request, "navigator/dashboard.html",{"total_orders":total_orders,
                                                       "total_sales":total_sales,
                                                       "monthly_active_users":monthly_active_users,
                                                       "new_clients_count":new_clients_count,})

def categories(request):
    cate = TableCategories.objects.all()
    return render(request, "navigator/categories.html",{"cate":cate})

def add_categories(request):
    return render(request, "navigator/add_categories.html")

def save_categories(request):
    if request.method == "POST":
        category = request.POST.get("category")
        image = request.FILES.get("image")
        status = request.POST.get("status")
        if TableCategories.objects.filter(category=category).exists():
            messages.error(request, "Category already exists")
            return redirect("add_categories")
        else:
            tab_obj = TableCategories(category=category, image=image, status=status)
            tab_obj.save()
            return redirect("categories")
    messages.error(request, "Invalid Request")
    return redirect("add_categories")


def edit_categories(request, cate_id):
    data = TableCategories.objects.get(id=cate_id)
    return render(request, "navigator/edit_categories.html", {"data":data})

def update_categories(request, cate_id):
    tab_obj = TableCategories.objects.get(id=cate_id)
    if request.method == "POST":
        category = request.POST.get("category")
        image = request.FILES.get("image") or tab_obj.image
        status = request.POST.get("status")
        if TableCategories.objects.filter(category=category).exclude(id=cate_id).exists():
            messages.error(request, "Category already exists")
            return redirect("update_categories", cate_id=cate_id)
        else:
            tab_obj.category = category
            tab_obj.image = image
            tab_obj.status = status
            tab_obj.save()
            return redirect("categories")
    return render(request, "navigator/edit_categories.html", {"data":tab_obj})

def delete_categories(request, cate_id):
    tab_obj = TableCategories.objects.get(id=cate_id)
    tab_obj.delete()
    return redirect("categories")

def sub_categories(request):
    sub = TableSubCategories.objects.all()
    return render(request, "navigator/sub_categories.html", {"sub":sub})

def add_sub_categories(request):
    cate = TableCategories.objects.all()
    return render(request, "navigator/add_sub_categories.html", {"cate":cate})

def save_sub_categories(request):
    if request.method == "POST":
        category_id = request.POST.get("category")
        sub_category = request.POST.get("sub_category")
        image = request.FILES.get("image")
        status = request.POST.get("status")
        if TableSubCategories.objects.filter(sub_category=sub_category).exists():
            messages.error(request, "Sub category already exists")
            return redirect("add_sub_categories")
        else:
            tab_obj = TableSubCategories(category_id=category_id, sub_category=sub_category, image=image, status=status)
            tab_obj.save()
            return redirect("sub_categories")
    else:
        return render(request, "navigator/add_sub_categories.html")

def edit_sub_categories(request, sub_id):
    data = TableSubCategories.objects.get(id=sub_id)
    cate = TableCategories.objects.all()
    return render(request, "navigator/edit_sub_categories.html", {"data":data,"cate":cate})

def update_sub_categories(request, sub_id):
    tab_obj = TableSubCategories.objects.get(id=sub_id)
    cate = TableCategories.objects.all()
    if request.method == "POST":
        category_id = request.POST.get("category")
        sub_category = request.POST.get("sub_category")
        image = request.FILES.get("image") or tab_obj.image
        status = request.POST.get("status")
        tab_obj.category_id = category_id
        tab_obj.sub_category = sub_category
        tab_obj.image = image
        tab_obj.status = status
        if TableSubCategories.objects.filter(category_id=category_id,sub_category=sub_category).exclude(id=sub_id).exists():
            messages.error(request, "Sub category in same category already exists")
            return render(request, "navigator/edit_sub_categories.html", {"data": tab_obj,"cate":cate})
        else:
            tab_obj.category_id = category_id
            tab_obj.sub_category = sub_category
            tab_obj.image = image
            tab_obj.status = status
            tab_obj.save()
            return redirect("sub_categories")
    else:
        return render(request, "navigator/edit_sub_categories.html", {"data":tab_obj,"cate":cate})

def delete_sub_categories(request, sub_id):
    tab_obj = TableSubCategories.objects.get(id=sub_id)
    tab_obj.delete()
    return redirect("sub_categories")

def blogs(request):
    blog = TableBlog.objects.all()
    return render(request, "navigator/blogs.html", {"blog":blog})

def add_blogs(request):
    sub = TableSubCategories.objects.all()
    return render(request, "navigator/add_blogs.html", {"sub":sub})

def save_blog(request):
    sub = TableSubCategories.objects.all()
    if request.method == "POST":
        sub_category_id = request.POST.get("sub_category")
        blog_title = request.POST.get("blog_title")
        content = request.POST.get("content")
        image1 = request.FILES.get("image1")
        sub_content = request.POST.get("sub_content")
        title2 = request.POST.get("title2")
        content2 = request.POST.get("content2")
        image2 = request.POST.get("image2")
        sub_content2 = request.POST.get("sub_content2")
        summary_title = request.POST.get("summary_title")
        summary_content = request.POST.get("summary_content")
        tag = request.POST.get("tag")
        status = request.POST.get("status")
        slug = blog_title.replace(" ","-")
        if TableBlog.objects.filter(sub_category_id=sub_category_id, blog_title=blog_title).exists():
            messages.error(request, "Blog already exists in this sub category")
            return redirect("add_blogs")
        else:
            tab_obj = TableBlog()
            tab_obj.sub_category_id = sub_category_id
            tab_obj.blog_title = blog_title
            tab_obj.content = content
            tab_obj.image1 = image1
            tab_obj.sub_content = sub_content
            tab_obj.title2 = title2
            tab_obj.content2 = content2
            tab_obj.image2 = image2
            tab_obj.sub_content2 = sub_content2
            tab_obj.summary_title = summary_title
            tab_obj.summary_content = summary_content
            tab_obj.tag = tag
            tab_obj.status = status
            tab_obj.slug = slug.lower()
            tab_obj.save()
            return redirect("blogs")
    else:
        return render(request, "navigator/add_blogs.html",{"sub":sub})

def edit_blogs(request, blog_id):
    data = TableBlog.objects.get(id=blog_id)
    sub = TableSubCategories.objects.all()
    return render(request, "navigator/edit_blogs.html", {"data":data,"sub":sub})

def update_blog(request, blog_id):
    tab_obj = TableBlog.objects.get(id=blog_id)
    sub = TableSubCategories.objects.all()
    if request.method == "POST":
        sub_category_id = request.POST.get("sub_category")
        blog_title = request.POST.get("blog_title")
        content = request.POST.get("content")
        image1 = request.FILES.get("image1") or tab_obj.image1
        sub_content = request.POST.get("sub_content")
        title2 = request.POST.get("title2")
        content2 = request.POST.get("content2")
        image2 = request.POST.get("image2")
        sub_content2 = request.POST.get("sub_content2")
        summary_title = request.POST.get("summary_title")
        summary_content = request.POST.get("summary_content")
        tag = request.POST.get("tag")
        status = request.POST.get("status")
        slug = blog_title.replace(" ","-")
        if TableBlog.objects.filter(sub_category_id=sub_category_id, blog_title=blog_title).exclude(id=blog_id).exists():
            messages.error(request, "Blog already exists in this sub category")
            return render(request, "navigator/edit_blogs.html", {"data":tab_obj,"sub":sub})
        else:
            tab_obj.sub_category_id = sub_category_id
            tab_obj.blog_title = blog_title
            tab_obj.content = content
            tab_obj.image1 = image1
            tab_obj.sub_content = sub_content
            tab_obj.title2 = title2
            tab_obj.content2 = content2
            tab_obj.image2 = image2
            tab_obj.sub_content2 = sub_content2
            tab_obj.summary_title = summary_title
            tab_obj.summary_content = summary_content
            tab_obj.tag = tag
            tab_obj.status = status
            tab_obj.slug = slug.lower()
            tab_obj.save()
            return redirect("blogs")
    else:
        return render(request, "navigator/edit_blogs.html", {"data":tab_obj,"sub":sub})

def delete_blogs(request, blog_id):
    tab_obj = TableBlog.objects.get(id=blog_id)
    tab_obj.delete()
    return redirect("blogs")

def travel_packages(request):
    sort_by =  request.GET.get("sort", "-id")
    pac =TableTravelPackages.objects.all().order_by(sort_by)

    q_general = request.GET.get("general")
    q_duration = request.GET.get("duration")
    q_min_price = request.GET.get("min_price")
    q_max_price = request.GET.get("max_price")
    q_date = request.GET.get("date")

    if q_general:
        pac = pac.filter(
            Q(title__icontains=q_general) |
            Q(destination__icontains=q_general) |
            Q(type__icontains=q_general)
        )
    if q_duration:
        pac = pac.filter(duration__icontains=q_duration)
    if q_min_price:
        pac = pac.filter(price__gte=q_min_price)
    if q_max_price:
        pac = pac.filter(price__lte=q_max_price)
    if q_date:
        pac = pac.filter(date=q_date)

    paginator = Paginator(pac, 10)
    page_number = request.GET.get('page')
    pac = paginator.get_page(page_number)

    get_copy = request.GET.copy()
    if 'page' in get_copy:
        del get_copy['page']
    fixed_query_params = get_copy.urlencode()

    return render(request, "navigator/travel_packages.html", {"pac":pac,
                                                              "fixed_query_params":fixed_query_params,
                                                              "current_sort":sort_by,})

def add_travel_packages(request):
    return render(request, "navigator/add_travel_packages.html")

def save_travel_packages(request):
    if request.method == "POST":
        title = request.POST.get("title")
        slug = title.replace(" ","-")
        if TableTravelPackages.objects.filter(title=title).exists():
            messages.error(request, "Travel package title already exists")
            return render(request, "navigator/add_travel_packages.html")
        else:
            tab_obj = TableTravelPackages()
            tab_obj.title = title
            tab_obj.tagline = request.POST.get("tagline")
            tab_obj.slug = slug.lower()
            tab_obj.destination = request.POST.get("destination")
            tab_obj.description = request.POST.get("description")
            tab_obj.duration = request.POST.get("duration")
            tab_obj.display_price = request.POST.get("display_price")
            tab_obj.price = request.POST.get("price")
            tab_obj.price_for = request.POST.get("price_for")
            tab_obj.type = request.POST.get("type")
            tab_obj.status = request.POST.get("status")
            tab_obj.save()

            images = request.FILES.getlist("images")
            for img in images:
                pic = TableTravelPackagesMedia()
                pic.title_id = tab_obj.id
                pic.images = img
                pic.save()

            return redirect("travel_packages")
    else:
        return render(request, "navigator/add_travel_packages.html")

def edit_travel_packages(request, pac_id):
    data = TableTravelPackages.objects.get(id=pac_id)
    images = TableTravelPackagesMedia.objects.filter(title_id=pac_id)
    return render(request, "navigator/edit_travel_packages.html", {"data":data,"images":images})

def update_travel_packages(request, pac_id):
    tab_obj = TableTravelPackages.objects.get(id=pac_id)
    if request.method == "POST":
        title = request.POST.get("title")
        slug = title.replace(" ","-")
        tagline = request.POST.get("tagline")
        destination = request.POST.get("destination")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        tab_obj.display_price = request.POST.get("display_price")
        price = request.POST.get("price")
        price_for = request.POST.get("price_for")
        type = request.POST.get("type")
        status = request.POST.get("status")
        if TableTravelPackages.objects.filter(title=title).exclude(id=pac_id).exists():
            messages.error(request, "Travel package title already exists")
            images = TableTravelPackagesMedia.objects.filter(title_id=pac_id)
            return render(request, "navigator/edit_travel_packages.html", {"data":tab_obj,"images":images})
        else:
            tab_obj.title = title
            tab_obj.slug = slug.lower()
            tab_obj.tagline = tagline
            tab_obj.destination = destination
            tab_obj.description = description
            tab_obj.duration = duration
            tab_obj.price = price
            tab_obj.price_for = price_for
            tab_obj.type = type
            tab_obj.status = status
            tab_obj.save()

            images = request.FILES.getlist("images")
            for img in images:
                TableTravelPackagesMedia.objects.create(title_id=tab_obj.id, images=img)
            return redirect("travel_packages")
    else:
        images = TableTravelPackagesMedia.objects.filter(title_id=tab_obj.id)
        return render(request, "navigator/edit_travel_packages.html", {"data":tab_obj,"images":images})


def delete_package_image(request, img_id):
    if request.method == "POST":
        try:
            img_obj = TableTravelPackagesMedia.objects.get(id=img_id)
            img_obj.delete()
            return JsonResponse({"success": True})
        except TableTravelPackagesMedia.DoesNotExist:
            return JsonResponse({"success": False, "error": "Image not found"})
    return JsonResponse({"success": False, "error": "Invalid request"})

def delete_travel_packages(request, pac_id):
    tab_obj = TableTravelPackages.objects.get(id=pac_id)
    tab_obj.delete()
    return redirect("travel_packages")

def orders(request):
    tour = TableTourPurchased.objects.all().order_by('-id')[:1]
    completed_order_count = TableTourPurchased.objects.filter(order_status="Completed").count()
    completed_sales = sum(i.price for i in TableTourPurchased.objects.filter(order_status="Completed"))
    return render(request, "navigator/orders.html",{"tour":tour,"show_view_all": True,
                                                    "completed_order_count":completed_order_count,
                                                    "completed_sales":completed_sales})

def view_all_orders(request):
    sort_by = request.GET.get("sort", "-id")
    tour = TableTourPurchased.objects.all().order_by(sort_by)

    q_search = request.GET.get('search_general')
    q_status = request.GET.get('status')
    q_checkin = request.GET.get('checkin_date')
    q_purchase = request.GET.get('purchase_date')
    q_check_month = request.GET.get('checkin_month')
    q_purchase_month = request.GET.get('purchase_month')

    if q_search:
        tour = tour.filter(Q(package__title__icontains=q_search) |
                           Q(package__destination__icontains=q_search) |
                           Q(address__fullname__icontains=q_search) |
                           Q(order_id__icontains=q_search) )
    if q_status:
        tour = tour.filter(order_status__icontains=q_status)
    if q_checkin:
        tour = tour.filter(checkin_date__icontains=q_checkin)
    if q_purchase:
        tour = tour.filter(invoice_date__icontains=q_purchase)
    if q_check_month:
        year, month = q_check_month.split('-')
        tour = tour.filter(checkin_date__year=int(year), checkin_date__month=int(month))
    if q_purchase_month:
        year, month = q_purchase_month.split('-')
        tour = tour.filter(invoice_date__year=int(year), invoice_date__month=int(month))

    total_orders = tour.count()
    total_sales = sum(i.price for i in tour)
    completed_order_count = tour.filter(order_status="Completed").count()
    completed_sales = sum(i.price for i in tour.filter(order_status="Completed"))

    paginator = Paginator(tour, 7)
    page_number = request.GET.get('page')
    tour = paginator.get_page(page_number)

    get_copy = request.GET.copy()
    if "page" in get_copy:
        del get_copy["page"]
    fixed_query_params = get_copy.urlencode()

    return render(request, "navigator/all_orders.html",{"tour":tour,
                                                        "completed_order_count":completed_order_count,
                                                        "completed_sales":completed_sales,
                                                        "total_orders":total_orders,"total_sales":total_sales,
                                                        "fixed_query_params":fixed_query_params,
                                                        "current_sort":sort_by,})

def export_orders_csv(request):
    q_search = request.GET.get('search_general')
    q_status = request.GET.get('status')
    q_checkin = request.GET.get('checkin_date')
    q_purchase = request.GET.get('purchase_date')
    q_check_month = request.GET.get('checkin_month')
    q_purchase_month = request.GET.get('purchase_month')

    tour = TableTourPurchased.objects.all().order_by('-id')

    if q_search:
        tour = tour.filter(Q(package__title__icontains=q_search) |
                           Q(package__destination__icontains=q_search) |
                           Q(address__fullname__icontains=q_search) |
                           Q(order_id__icontains=q_search))
    if q_status:
        tour = tour.filter(order_status__icontains=q_status)
    if q_checkin:
        tour = tour.filter(checkin_date__icontains=q_checkin)
    if q_purchase:
        tour = tour.filter(invoice_date__icontains=q_purchase)
    if q_check_month:
        year, month = q_check_month.split('-')
        tour = tour.filter(checkin_date__year=int(year), checkin_date__month=int(month))
    if q_purchase_month:
        year, month = q_purchase_month.split('-')
        tour = tour.filter(invoice_date__year=int(year), invoice_date__month=int(month))

    today = datetime.date.today().strftime('%Y-%m-%d')
    order_file = f"orders_{today}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={order_file}'
    writer = csv.writer(response)
    writer.writerow(["Order ID","Customer", "Email", "Phone Number", "Address", "City", "District",
                    "State", "Postcode", "Title", "Destination", "Duration", "Status",
                    "Check-in Date","Check-in Time", "Purchase Date", "Headcount", "Price", "Display Price",
                    "Room Type", "Energetic at", "Vibe", "Note"])

    for i in tour:
        writer.writerow(
            [
                i.order_id,
                i.address.fullname,
                i.address.email,
                i.address.phone,
                i.address.address,
                i.address.city,
                i.address.district,
                i.address.state,
                i.address.postcode,
                i.package.title,
                i.package.destination,
                i.package.duration,
                i.order_status,
                i.checkin_date,
                i.checkin_time,
                i.invoice_date,
                i.headcount,
                i.price,
                i.display_price,
                i.room_type,
                i.energy_level,
                i.vibe,
                i.notes
            ]
        )
    return response


def delete_order(request, order_id):
    data = TableTourPurchased.objects.get(id=order_id)
    data.delete()
    return redirect("orders")

def invoice(request,order_id):
    data = TableTourPurchased.objects.get(id=order_id)
    discount = int(data.display_price - data.price)
    return render(request, "navigator/invoice.html",{"data":data,"discount":discount})

def change_order_status(request, order_id):
    if request.method == "POST":
        order = TableTourPurchased.objects.get(id=order_id)
        new_status = request.POST.get("order_status")
        order.order_status = new_status
        order.save()
        return redirect("orders")
    messages.error(request, "Invalid Request")
    return redirect("orders")


