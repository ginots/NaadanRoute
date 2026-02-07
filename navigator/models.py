from django.db import models
from django.db.models import ForeignKey, Model

# Create your models here.

class TableCategories(models.Model):
    category = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="categories/", null=True)
    status = models.CharField(max_length=100, null=True)

class TableSubCategories(models.Model):
    category = models.ForeignKey(TableCategories, on_delete=models.CASCADE, null=True, related_name="subs")
    sub_category = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="sub_categories/", null=True)
    status = models.CharField(max_length=100, null=True)

class TableBlog(models.Model):
    sub_category = models.ForeignKey(TableSubCategories, on_delete=models.CASCADE, null=True)
    blog_title =models.CharField(max_length=100, null=True)
    content = models.TextField(null=True)
    image1 = models.ImageField(upload_to="blog/", null=True)
    sub_content = models.TextField( null=True)
    title2 = models.CharField(max_length=100, null=True)
    content2 = models.TextField(null=True)
    image2 = models.ImageField(upload_to="blog/", null=True)
    sub_content2 = models.TextField( null=True)
    summary_title = models.CharField(max_length=100, null=True)
    summary_content = models.TextField(null=True)
    tag = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    date = models.DateField(null=True, auto_now_add=True)

class TableTravelPackages(models.Model):
    title = models.CharField(max_length=100, null=True)
    tagline = models.CharField(max_length=100, null=True)
    destination = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    duration = models.CharField(max_length=100, null=True)
    display_price = models.FloatField(max_length=100, null=True)
    price = models.FloatField(max_length=100, null=True)
    price_for = models.CharField(max_length=100, null=True)
    type = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True)
    slug = models.SlugField(max_length=100, blank=True)
    date = models.DateField(null=True, auto_now_add=True)

class TableTravelPackagesMedia(models.Model):
    title = models.ForeignKey(TableTravelPackages, on_delete=models.CASCADE, null=True, related_name="media")
    images = models.ImageField(upload_to="travel_packages/", null=True)