from django.db import models
from django.conf import settings

from navigator.models import TableTravelPackages


# Create your models here.

class TableWishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    package = models.ForeignKey(TableTravelPackages, on_delete=models.CASCADE, related_name="wishlisted_package")
