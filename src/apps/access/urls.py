from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import login_user, logout_view, register_user
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_user, name='register'),
]
