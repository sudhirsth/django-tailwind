from django.shortcuts import render
from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView, DeleteView
from .models import Role
from .forms import RoleForm
from ..user.models import User
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse


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

    return render(request, 'apps/authorization/manage_roles.html', context)


def manage_groups_add(request):
    current_group = Group()
    permissions = Permission.objects.all()
    if request.method == 'POST':
        group_name = request.POST.get("name")
        if group_name != "":
            if len(Group.objects.filter(name=group_name)) == 0:

                # Processing the main form data
                current_group.name = group_name
                current_group.save()

                # Processing the related many-to-many field
                checked_permissions_ids = request.POST.getlist(
                    "chk_permission")
                valid_permissions = Permission.objects.filter(
                    id__in=checked_permissions_ids)
                print(valid_permissions)
                current_group.permissions.set(valid_permissions)

            else:
                messages.error(
                    request, f'Group named "{group_name}" already exists')
                return redirect('manage_groups')

            messages.success(request, 'Group added successfully')

        return redirect('groups')

    context = {
        'permissions': permissions,
        'current_group': current_group
    }

    return render(request, 'apps/authorization/manage_groups.html', context)


def manage_groups_edit(request, id):
    try:
        current_group = Group.objects.get(id=id)
        permissions = Permission.objects.all()

        if request.method == 'POST':
            group_name = request.POST.get("name")
            if group_name != "":
                current_group.name = group_name
                current_group.save()

                # Processing the related many-to-many field
                checked_permissions_ids = request.POST.getlist(
                    "chk_permission")
                valid_permissions = Permission.objects.filter(
                    id__in=checked_permissions_ids)
                print(valid_permissions)
                current_group.permissions.set(valid_permissions)

                messages.success(request, 'Group updated successfully')

            return redirect('groups')

        context = {
            'current_group': current_group,
            'permissions': permissions
        }

        return render(request, 'apps/authorization/manage_groups.html', context)

    except Group.DoesNotExist:
        # Object does not exist
        # Redirect to Not exist page
        pass


def delete_groups(request, id):
    group = Group.objects.filter(id=id)
    if len(group) > 0:
        group.delete()
        messages.success(request, "Group deleted successfully.")
    else:
        messages.error(request, "Group not found")
    return redirect("groups")


class delete_group(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("user_list")
    template_name = 'apps/authorization/group_list.html'

    def delete(self, request, *args, **kwargs):
        # if request.is_ajax():
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'message': 'User deleted successfully'})
        # return super().delete(request, *args, **kwargs)
