from django.shortcuts import render

# Create your views here.
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.views.generic import View, TemplateView
from .models import Role
from .forms import RoleForm


def roles_list(request):
    roles = Role.objects.all()
    return render(request, 'apps/authorization/role_list.html', {'roles': roles})

def group_list(request):
    groups = Group.objects.all()
    return render(request, 'apps/authorization/group_list.html', {'groups': groups})


def manage_roles(request):
    permissions = Permission.objects.all()

    if request.method == 'POST':
        checked_permissions_list = request.POST.getlist("chk_permission")
        role_name = request.POST.get("name")
        alias = request.POST.get("alias")
        is_active = request.POST.get("is_active")

        if role_name != "":
            role = Role(name=role_name, alias=alias,
                        permissions=checked_permissions_list)

            role.save()
            print(checked_permissions_list)

            messages.success(request, 'Role saved successfully')

        return redirect('roles')

    # else:
    #     form = RoleForm()

    # roles = Role.objects.all()
    context = {
        # 'form': form,
        # 'roles': roles,
        'permissions': permissions
    }

    return render(request, 'apps/authorization/manageroles.html', context)


def manage_groups(request):
    permissions = Permission.objects.all()
    groups = Group.objects.all()
    if request.method == 'POST':
        checked_permissions_list = request.POST.getlist("chk_permission")
        group_name = request.POST.get("name")

        if group_name != "":
            group = Group(name=group_name)
            group.save()
           
            messages.success(request, 'Group saved successfully')

        return redirect('managegroups')

    # else:
    #     form = RoleForm()

    # roles = Role.objects.all()
    context = {
        # 'form': form,
        'groups': groups,
        'permissions': permissions
    }

    return render(request, 'apps/authorization/managegroups.html', context)
