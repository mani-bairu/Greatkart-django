from django.contrib import admin
from .models import *

# Register your models here.

class cartidadmin(admin.ModelAdmin):
    list_display=['cart_id','date_added']
admin.site.register(Cart,cartidadmin)

class cartitemsadmin(admin.ModelAdmin):
    list_display=['product','cart','quantity','is_active']
admin.site.register(Cart_items,cartitemsadmin)
