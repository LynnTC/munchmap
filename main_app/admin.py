from django.contrib import admin

# Register your models here.

from .models import Restaurant, Review

admin.site.register(Restaurant)

admin.site.register(Review)