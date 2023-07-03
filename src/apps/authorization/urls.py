from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import manage_roles, roles_list, manage_groups, group_list
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('authorization/roles/', roles_list, name="roles"),
    path('authorization/roles/manage', manage_roles, name="manageroles"),
    path('authorization/groups/', group_list, name="groups"),
    path('authorization/groups/manage', manage_groups, name="managegroups"),

]
