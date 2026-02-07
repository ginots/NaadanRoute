from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, Model
from django.conf import settings

from navigator.models import TableTravelPackages


# Create your models here.
class TableAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=100, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    city = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postcode = models.IntegerField(null=True)

class TableTourPurchased(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(TableAddress, on_delete=models.CASCADE)
    package = models.ForeignKey(TableTravelPackages, on_delete=models.CASCADE)
    headcount = models.IntegerField(null=True,default=0)
    price = models.FloatField(null=True, default=0)
    display_price = models.FloatField(null=True, default=0)
    checkin_date = models.DateField(null=True)
    checkin_time = models.TimeField(null=True)
    room_type = models.CharField(max_length=100, null=True)
    energy_level = models.CharField(max_length=100, null=True)
    vibe = models.CharField(max_length=100, null=True)
    notes = models.TextField(null=True)
    invoice_date = models.DateField(null=True, auto_now_add=True)
    order_id = models.CharField(max_length=100, null=True)
    payment_id = models.CharField(max_length=100, null=True)
    order_status = models.CharField(max_length=20, null=True)
    payment_method = models.CharField(max_length=100, null=True)
    payment_status = models.CharField(max_length=20, null=True)

class TableChatMessages(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    session_id = models.CharField(max_length=100, null=True)
    role = models.CharField(max_length=100, choices=[("user", "User"),("kera","Kera")])
    content = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["timestamp"]
