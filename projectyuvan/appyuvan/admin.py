from django.contrib import admin
from appyuvan.models import Products
#admin.site.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display=['name','price','cat']
    list_filter=['price','is_active']

admin.site.register(Products,ProductsAdmin)