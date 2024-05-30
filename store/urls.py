
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.Store,name='store'),
    path('<slug:category_slug>/',views.Store,name='get_product_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='product_detail'),
    path('search/keyword',views.search,name='search'),



   
]
