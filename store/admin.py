from django.contrib import admin
from .models import Product,variations

# Register your models here.

class productadmin(admin.ModelAdmin):
    prepopulated_fields = { "slug" : ["product_name",]}
    list_display = ['product_name','price','stock','is_avalible']

admin.site.register(Product,productadmin)

class variationadmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)

admin.site.register(variations,variationadmin)