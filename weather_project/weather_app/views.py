from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, CityForm, NotificationForm, UserRegistrationForm
from .models import WeatherNotification, CustomUser
import requests
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import os
from .weather import get_weather
from django.shortcuts import redirect
from .tasks import send_weather_email
from django.contrib import messages

def trigger_weather_email(request):
    
    send_weather_email.delay()  # Run Celery task asynchronously
    messages.success(request, "Weather notification emails have been sent!")
    return redirect('weather')


User = get_user_model()


# Weather ID-based alert messages
WEATHER_ALERTS = {
    "Thunderstorm": " Thunderstorm detected! Protect your Crops",
    "Drizzle": "Light drizzle outside. Your Plants are happy",
    "Rain": "Rainy weather! Look for good drainage to protect your crops",
    "Snow": "Snowfall expected. Protect your Crops",
    "Atmosphere": "Foggy conditions.",
    "Clear": "Clear sky! It's a great day to for your plants",
    "Clouds": "Cloudy skies today.",
}






# Use environment variable for API key
from django.conf import settings
OPENWEATHER_API_KEY = settings.OPENWEATHER_API_KEY

def home(request):
    return render(request, 'weather_app/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('enter_city')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'weather_app/register.html', {'form': form})  

def user_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            login(request, user)
            return redirect('enter_city')
    return render(request, 'weather_app/login.html')

def enter_city(request):
    if request.method == 'POST':
        city_name = request.POST['city']
        request.user.city = city_name  # 
        request.user.save()
        return redirect('weather')  # Redirect to the weather page

    return render(request, 'weather_app/enter_city.html')


"""def weather(request):
    print("\n weather() view called!")  # Debugging print

    if not request.user.city:
        return redirect('enter_city')

    city = request.user.city
    print(f"\n Fetching weather for city: {city}")  # Debugging print

    weather_data = get_weather(city)  #  Correctly calling get_weather()

    return render(request, 'weather_app/weather.html', {'weather_data': weather_data})"""



def weather(request):
    """Fetch and display weather data with alerts."""
    if not request.user.city:
        return redirect('enter_city')

    city = request.user.city
    weather_data = get_weather(city)  # Fetch data from OpenWeather API

    # Extract weather ID and determine alert
    weather_alert = "No severe weather alerts."
    if "weather" in weather_data and weather_data["weather"]:
        weather_main = weather_data["weather"][0]["main"]  # Extract main weather condition
        weather_id = weather_data["weather"][0]["id"]  # Extract weather ID

        # Assign alert based on weather category
        if 200 <= weather_id <= 232:
            weather_alert = "Thunderstorm detected! Protect your Crops"
        elif 300 <= weather_id <= 321:
            weather_alert = "Light drizzle outside. Your Plants are happy"
        elif 500 <= weather_id <= 531:
            weather_alert = "Rainy weather! Look for good drainage to protect your crops"
        elif 600 <= weather_id <= 622:
            weather_alert = "Snowfall expected. Protect your Crops"
        elif 701 <= weather_id <= 781:
            weather_alert = "Foggy conditions."
        elif weather_id == 800:
            weather_alert = "Clear sky! It's a great day to for your plants"
        elif 801 <= weather_id <= 804:
            weather_alert = "Cloudy skies today."
        
    return render(request, 'weather_app/weather.html', {'weather_data': weather_data, 'weather_alert': weather_alert})

def set_notification(request):
    """Allow users to set weather notifications."""
    if request.method == "POST":
        form = NotificationForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.user = request.user
            notification.save()
            return redirect('weather')
    else:
        form = NotificationForm()
    return render(request, 'weather_app/set_notification.html', {'form': form})
