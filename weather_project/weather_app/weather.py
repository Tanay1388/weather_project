"""import requests
from django.conf import settings
#import os

API_KEY = '8ab77d733e192e0004a1a4240015d95e'

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch weather data"}

#curl "http://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=8ab77d733e192e0004a1a4240015d95e&units=metric"
#curl "http://api.openweathermap.org/data/2.5/weather?q=Mumbai&appid=8ab77d733e192e0004a1a4240015d95e&units=metric"""""
from django.conf import settings
import requests

def get_weather(city):
    print("\n get_weather() function called!")  # Debugging print
    api_key = settings.OPENWEATHER_API_KEY  #  Use settings API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        response_data = response.json()

        #  Print API request and response in console for debugging
        print(f"\n🔹 API Request URL: {url}")
        print(f"🔹 Response Code: {response.status_code}")
        print(f"🔹 Response Data: {response_data}\n")

        if response.status_code == 200:
            return response_data
        else:
            return {"error": response_data.get("message", "Unknown API error")}

    except Exception as e:
        print(f"\n Error fetching weather data: {e}\n")
        return {"error": "Failed to connect to OpenWeather API"}

