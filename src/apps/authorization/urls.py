from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from .views import manage_roles, roles_list, manage_groups_add, group_list,manage_groups_edit,delete_groups
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('authorization/roles/', roles_list, name="roles"),
    path('authorization/roles/manage', manage_roles, name="manage_roles"),
    path('authorization/groups/', group_list, name="groups"),
    path('authorization/groups/manage', manage_groups_add, name="manage_groups"),
    path('authorization/groups/manage/<int:id>', manage_groups_edit, name="manage_groups"),
    path('authorization/groups/delete/<int:id>', delete_groups, name="delete_groups"),

]
