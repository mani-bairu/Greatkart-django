
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.cart,name='cart'),
    path('add_cart/<int:product_id>/',views.add_cart,name='add_cart'),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',views.remove_cart,name='remove_cart'),
    path('add_cart_quantity/<int:product_id>/<int:cart_item_id>/',views.add_cart_quantity,name='add_cart_quantity'),

    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',views.delete_cart_item,name='delete_cart_item'),




]
