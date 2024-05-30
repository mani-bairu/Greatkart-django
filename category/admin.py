from django.contrib import admin
from .models import Category

# Register your models here.

class categoryadmin(admin.ModelAdmin):
    prepopulated_fields={ 'slug' : ['caterogy_name'],}
    list_display = ['caterogy_name',]
admin.site.register(Category,categoryadmin)