from django import forms
from .models import Role
from django.contrib.auth.models import Permission
from django.forms.widgets import CheckboxSelectMultiple


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name='multiple_select_checkbox.html'

class RoleForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "type": "text",
                "placeholder": "Manager",
                "class": "bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        )
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = CustomCheckboxSelectMultiple
    )
    class Meta:
        model=Role
        fields=['name','permissions']