from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('blogs/', views.blogview.as_view(), name='landing_blog'),
]
