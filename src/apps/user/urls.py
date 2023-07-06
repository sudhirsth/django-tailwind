from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import login_user, logout_view, register_user, user_list, user_groups, create_user, delete_user,update_userprofile
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', login_user, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_user, name='register'),
    path('users/', user_list.as_view(), name="user_list"),
    path('users/groups/<id>', user_groups.as_view(), name="user_groups"),
    path('users/create/', create_user.as_view(), name="user_create"),
    path('users/delete/<int:id>/', delete_user.as_view(), name='delete_user'),
    path('users/profile/', update_userprofile.as_view(), name='user_profile')



]
