
from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('signin/',views.signin,name='signin'),
    path('logout/',views.logout,name='logout'),
    path('resetnewpassword/',views.resetnewpassword,name='resetnewpassword'),


    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    path('resetpassword/<uidb64>/<token>/',views.resetpassword,name='resetpassword'),

    path('forgotpassword/',views.forgotpassword,name='forgotpassword'),


    path('dashboard/',views.dashboard,name='dashboard'),



   




]
