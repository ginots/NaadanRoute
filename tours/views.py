import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from navigator.models import TableTravelPackages,TableTravelPackagesMedia
from django.contrib import messages
import razorpay
from datetime import time
from django.core.paginator import Paginator
from django.db.models import Q

from tours.models import *

from accounts.models import TableWishlist

import google.generativeai as genai
import json
from django.http import JsonResponse
import os
from django.conf import settings



razorpay_client = razorpay.Client(
                    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
                )

# Create your views here.
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ai_chat(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_message = data.get("message","")

            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key

            TableChatMessages.objects.create(
                user = request.user if request.user.is_authenticated else None,
                session_id = session_key,
                role = "user",
                content=user_message,
            )
            history_obj = TableChatMessages.objects.filter(session_id = session_key).order_by("-timestamp")[:10]
            formatted_history = ""
            for i in reversed(history_obj):
                role_label = "Sanchari" if i.role == "user" else "Kera"
                formatted_history += f"{role_label}: {i.content}\n"

            pac = TableTravelPackages.objects.filter(status="Active")
            pac_context = ""
            for i in pac:
                pac_context += f"ID:{i.id}, Title:{i.title}, Destination:{i.destination}, Type:{i.type}, Desc:{i.description[:100]}\n"
            system_prompt = f"""
            You are Kera, a warm, soulful Kerala Travel Expert, designed by NaadanRoute, a website for travellers
            seeking meaningful journeys in Kerala. 
            You don't just sell tours; you match destinations to human emotions.
    
            ### YOUR PERSONALITY:
            - Use warm, empathetic language.
            - Use occasional Malayalam words like 'Namaskaram' (Hello) or 'Santhosham' (Happiness) 
              or 'Sanchari' (Traveller). 
            - If a user is sad/stressed, be a healer. If they are excited, be their cheerleader.
            
            ### YOUR GOAL:
            Gather enough information to make a perfect match. Do not recommend a package in the first message unless the user has already provided their needs.
            
            ### INFORMATION YOU NEED (The Checklist):
            1. Current Vibe/Feeling (e.g., stressed, adventurous, romantic).
            2. Expectations (e.g., quiet, luxury, culture, wildlife).
            3. Preferred Destination or landscape (e.g., hills, backwaters, beaches).
            4. Duration & Type (e.g., short weekend, long family trip).
            
            ### THE MISSION:
            1. Analyze the user's message. 
            2. If information is missing, ask one or two friendly follow-up questions to complete the "Checklist". Set 'suggested_package_id' to null.
            3. Once you have a clear picture of their needs, select the most suitable ID from the AVAILABLE PACKAGES below.
            
            AVAILABLE PACKAGES:
            {pac_context}
    
            ### RESPONSE FORMAT:
            You must respond in valid JSON format:
            {{
                "reply": "Your warm, empathetic response to the user's feelings",
                "suggested_package_id": 123
            }}
            """
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            full_query = f"{formatted_history}\nKera:"
            response = model.generate_content(system_prompt + full_query)
            ai_text = response.text
            match = re.search(r'\{.*\}', ai_text, re.DOTALL)
            if match:
                try:
                    ai_data = json.loads(match.group())
                    kera_reply = ai_data.get("reply","Namaskaram! Let's explore Kerala.")
                    package_id = ai_data.get("suggested_package_id")
                except json.JSONDecodeError:
                    kera_reply = ai_text
                    package_id = None
            else:
                kera_reply = ai_text
                package_id = None

            TableChatMessages.objects.create(
                user = request.user if request.user.is_authenticated else None,
                session_id = request.session.session_key,
                role = "kera",
                content=kera_reply,
            )
            return JsonResponse(
                {"reply": kera_reply, "package_id": package_id}
            )


        except Exception as e:
            print(f"--- KERA ERROR LOG: {e} ---")
            return JsonResponse({
                    "reply": "Apologies, I'm currently too busy at the moment. Let's chat again after a few moments. I'd love to help you choose your dream journey. Veendum Kaanaam!",
                "package_id": None
            })

    return JsonResponse({"error": "Invalid request"}, status=400)

def tours_dashboard(request):
    pac = TableTravelPackages.objects.filter(status="Active").prefetch_related("media").order_by('-id')
    packages = TableTravelPackages.objects.all()
    session_key = request.session.session_key
    chat_history = []
    if session_key:
        chat_history = TableChatMessages.objects.filter(session_id = session_key).order_by("timestamp")

    recommended_id = request.GET.get("recommended")
    recommended_pkg = None
    if recommended_id and recommended_id != "null":
        recommended_pkg = TableTravelPackages.objects.filter(id=recommended_id).first()
        if recommended_pkg:
            pac = pac.exclude(id=recommended_id)

    paginator = Paginator(pac, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    wishlist_ids = []

    if request.user.is_authenticated:
        wishlist_ids = TableWishlist.objects.filter(user_id=request.user).values_list("package_id", flat=True)

    return render(request, "tours/tours_dashboard.html", {"pac": page_obj,
                                                          "packages": packages, "recommended_pkg": recommended_pkg,
                                                          "wishlist_ids": wishlist_ids,
                                                          "chat_history": chat_history})

def tours_details(request,package_slug):
    data = TableTravelPackages.objects.get(slug=package_slug)
    discount = int(data.display_price-data.price)

    return render(request, "tours/tours_details.html", {"data": data,
                                                        "discount": discount,})

@login_required
def book_now(request,package_slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_address = TableAddress.objects.filter(user=request.user)
            data = TableTravelPackages.objects.get(slug=package_slug)
            headcount = int(request.POST.get("headcount"))
            currency = 'INR'
            total = data.price * headcount
            display_price_sum = data.display_price * headcount
            amount = int(total) * 100
            razorpay_order = razorpay_client.order.create(dict(amount=amount, currency=currency,
                                                               payment_capture='0'))
            razorpay_order_id = razorpay_order["id"]
            return render(request, "tours/book_now.html", {"data": data,"headcount": headcount,
                                                "total":total,"display_price_sum":display_price_sum,
                                                "razorpay_order_id":razorpay_order_id,
                                                "razorpay_merchant_key": settings.RAZORPAY_KEY_ID,
                                                "razorpay_amount":amount,"currency":currency,
                                                "user_address":user_address,})
        else:
            return redirect("tours_details", package_slug=package_slug)
    else:
        messages.error(request, "Please login first")
        return redirect("tours_details", package_slug=package_slug)

from django.db import transaction
@login_required
def save_booking(request,tour_id):
    if request.method == "POST":
        user_address = request.POST.get("selected_address")
        razorpay_order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id', '')
        amount = request.POST.get('amount', '')
        purposes = request.POST.getlist("purpose")
        purpose_list = ", ".join(purposes)
        try:
            with transaction.atomic():
                razorpay_client.payment.capture(payment_id, amount)
                if user_address == "new":
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

                    obj = TableTourPurchased()
                    obj.user = request.user
                    obj.address_id = tab_obj.id
                    obj.package_id = tour_id
                    obj.headcount = request.POST.get("headcount")
                    obj.price = request.POST.get("price")
                    obj.display_price = request.POST.get("display_price")
                    obj.checkin_date = request.POST.get("date")
                    hour = int(request.POST.get("checkin_time_hour", 0))
                    minute = int(request.POST.get("checkin_time_minute", 0))
                    obj.checkin_time = time(hour, minute)
                    obj.room_type = request.POST.get("room_type")
                    obj.energy_level = request.POST.get("energy_level")
                    obj.vibe = purpose_list
                    obj.notes = request.POST.get("remark")
                    obj.order_id = razorpay_order_id
                    obj.payment_id = payment_id
                    obj.order_status = "ordered"
                    obj.payment_method = "online"
                    obj.payment_status = "paid"
                    obj.save()
                    messages.success(request, "Booking Successful!")
                    return redirect("/")
                else:
                    obj = TableTourPurchased()
                    obj.user = request.user
                    obj.address_id = user_address
                    obj.package_id = tour_id
                    obj.headcount = request.POST.get("headcount")
                    obj.price = request.POST.get("price")
                    obj.display_price = request.POST.get("display_price")
                    obj.checkin_date = request.POST.get("date")
                    hour = int(request.POST.get("checkin_time_hour", 0))
                    minute = int(request.POST.get("checkin_time_minute", 0))
                    obj.checkin_time = time(hour, minute)
                    obj.room_type = request.POST.get("room_type")
                    obj.energy_level = request.POST.get("energy_level")
                    obj.vibe = purpose_list
                    obj.notes = request.POST.get("remark")
                    obj.order_id = razorpay_order_id
                    obj.payment_id = payment_id
                    obj.order_status = "ordered"
                    obj.payment_method = "online"
                    obj.payment_status = "paid"
                    obj.save()
                    messages.success(request, "Booking Successful!")
                    return redirect("/")
        except Exception as e:
            messages.error(request, "Something went wrong with the booking record.")
            return redirect("/")
    messages.error(request, "Invalid Request")
    return redirect("/")





