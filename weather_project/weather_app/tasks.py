from django.core.mail import send_mail
from celery import shared_task
from .models import WeatherNotification
from .weather import get_weather
from django.conf import settings

@shared_task
def send_weather_email():
    notifications = WeatherNotification.objects.all()
    for notification in notifications:
        weather = get_weather(notification.city)
        if weather:
            subject = f"Weather Alert for {notification.city}"
            message = f"""
            Weather Update for {notification.city}:
            Temperature: {weather['main']['temp']}°C
            Condition: {weather['weather'][0]['description']}
            Wind Speed: {weather['wind']['speed']} m/s
            Humidity: {weather['main']['humidity']}%
            """
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  #Now using the correct email sender
                [notification.email],
                fail_silently=False
            )