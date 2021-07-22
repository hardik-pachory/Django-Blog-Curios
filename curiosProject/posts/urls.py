from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', post_list, name='list'),
    path('create/', post_create, name='create'),
    path('<int:id>/', post_detail, name='detail'),
    path('<int:id>/edit/', post_update, name='update'),
    path('<int:id>/delete/', post_delete)
]
app_name = 'posts'
