from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [
    path('',login_signup_page,name='startpage'),
    path('about/',about_page,name='about'),
    path('register/',register_page,name='register'),
    path('login/',login_page, name='login'),
    path('logout/',logout_page, name='logout'),
    #path('ques/',login_page, name='login'),
]