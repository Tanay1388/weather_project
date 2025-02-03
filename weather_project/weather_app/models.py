from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model (with a single city per user)
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Keep unique username
    city = models.CharField(max_length=100, blank=True, null=True)  # Store city as text
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class WeatherNotification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField()
    city = models.CharField(max_length=100)
    notification_time = models.TimeField()

    def __str__(self):
        return f"{self.email} - {self.city} at {self.notification_time}"
