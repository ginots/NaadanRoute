from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import TableTourPurchased


@shared_task
def send_booking_email(booking_id):
    booking = TableTourPurchased.objects.get(id=booking_id)

    subject = "Booking Confirmed - NaadanRoute 🌿"
    message = f"""
Hi {booking.user.first_name},

Your booking has been successfully confirmed!

Order ID: {booking.order_id}
Package: {booking.package.title}
Headcount: {booking.headcount}
Check-in Date: {booking.checkin_date}

Thank you for choosing NaadanRoute!
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [booking.user.email],
        fail_silently=False,
    )