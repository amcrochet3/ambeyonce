import requests
from django.conf import settings

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={settings.OPENWEATHER_API_KEY}&q={city}'
    response = requests.get(url)

    return response.json()