
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('enter_city/', views.enter_city, name='enter_city'),
    path('weather/', views.weather, name='weather'),
    path('set_notification/', views.set_notification, name='set_notification'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('send_notifications/', views.send_weather_email, name='send_notifications'),
    
]