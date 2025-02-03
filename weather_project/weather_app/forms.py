from django import forms
from django.core.exceptions import ValidationError
from .models import WeatherNotification, CustomUser  # 
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = CustomUser  # 
        fields = ['email', 'password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class CityForm(forms.ModelForm):
    class Meta:
        model = CustomUser  # 
        fields = ['city']

class NotificationForm(forms.ModelForm):
    class Meta:
        model = WeatherNotification
        fields = ['email', 'city', 'notification_time']

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
