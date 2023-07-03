from typing import Any, Dict
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, TemplateView
from .models import User


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
            messages.success(request, "You are registerd successfully and now logged in to the system.")
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


def user_profile(LoginRequiredMixin,request, pk):
    if request.user.is_authenticated:
        proifle = UserProfile.objects.get(user_id=pk)
        if request.method == "POST":
            current_user_profile = request.user.profile


class user_list(LoginRequiredMixin,TemplateView):
    template_name='apps/user/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # if user.is_superuser: #later check permission and if true list users with permission
        user = User.objects.all()
        print("Hello World From User Page")
        context["users"]=user
        return context

