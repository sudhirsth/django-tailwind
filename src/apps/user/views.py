from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, DeleteView, TemplateView, UpdateView, ListView, CreateView
from .models import User
from .forms import UserForm, UserProfileForm, CustomUserForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404


def login_user(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":

        if form.is_valid():
            username = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in successfully.')
                return redirect('/')
            else:
                messages.error(
                    request, 'Invalid Credentials.')
        else:
            messages.error(
                request, "Form is not valid. Please provide required fields.")

    return render(request, "apps/user/login.html", {"form": form})


def register_user(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(username=email, password=password)
            login(request, user)
            messages.success(
                request, "You are registerd successfully and now logged in to the system.")
            return redirect('/')
        else:
            messages.error(
                request, "Form is not valid. Please provide required fields.")
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, "apps/user/register.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You are logged out successfully.")
    return redirect('/')


def profile_list(LoginRequiredMixin, request):
    profiles = UserProfile.objects.exclude(user=request.user.email)
    return render(request, 'profile_list.html', {})


def user_profile(LoginRequiredMixin, request, pk):
    if request.user.is_authenticated:
        proifle = UserProfile.objects.get(user_id=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile


class user_list(LoginRequiredMixin, ListView):
    model = User
    template_name = 'apps/user/index.html'
    context_object_name = 'user_list'

# OR below using TemplateView
    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     # if user.is_superuser: #later check permission and if true list users with permission
    #     user = User.objects.all()
    #     print("Hello World From User Page")
    #     context["users"] = user
    #     return context

# Dynamic Filtering in ListView
# class PublisherBookListView(ListView):
#     template_name = "books/books_by_publisher.html"

#     def get_queryset(self):
#         self.publisher = get_object_or_404(Publisher, name=self.kwargs["publisher"])
#         return Book.objects.filter(publisher=self.publisher)

#     def get_context_data(self, **kwargs):
#     # Call the base implementation first to get a context
#     context = super().get_context_data(**kwargs)
#     # Add in the publisher
#     context["publisher"] = self.publisher
#     return context




class update_userprofile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'apps/user/user_profile.html'
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        user_profile, _ = UserProfile.objects.get_or_create(
            user=self.request.user)
        return user_profile

    def form_valid(self, form):
        user_profile = form.save(commit=False)
        user_profile.user = self.request.user

        if not user_profile.pk:
            user_profile.save()

        user_profile.user.first_name = form.cleaned_data['first_name']
        user_profile.user.last_name = form.cleaned_data['last_name']
        user_profile.user.save()
        messages.success(self.request, "User profile saved successfully.")
        return super().form_valid(form)


class user_groups(LoginRequiredMixin, View):
    # template_name = 'apps/user/user_groups.html'
    # model = User

    def get(self, request, id):
        user = User.objects.get(id=id)
        print(user.groups.all())
        groups = Group.objects.all()
        context = {'user': user, 'groups': groups}
        return render(request, 'apps/user/user_groups.html', context)

    def post(self, request, id):
        try:
            if request.method == 'POST':
                user = User.objects.get(id=id)

                checked_group_ids = request.POST.getlist(
                    "chkUserGroups")
                valid_groups = Group.objects.filter(id__in=checked_group_ids)
                user.groups.set(valid_groups)

                messages.success(
                    request, f'Groups updated for { user.email } successfully')

            return redirect("user_list")

        except User.DoesNotExist:
            pass


class create_user(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'apps/user/manage_user.html'
    success_url = reverse_lazy('user_list')

    def form_valid(self, form):
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        form.save_m2m()
        messages.success(self.request,"User added successfully.")
        return super().form_valid(form)

    def form_invalid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_invalid(form)


class delete_user(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy("user_list")
    template_name = 'apps/user/index.html'

    def delete(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        return super().delete(request, *args, **kwargs)
