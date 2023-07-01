from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import UserProfile
from django.contrib.auth.mixins import LoginRequiredMixin


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

    return render(request, "apps/access/login.html", {"form": form})


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
    return render(request, "apps/access/register.html", context)


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
