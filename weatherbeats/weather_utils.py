import requests
from django.conf import settings



api_key = settings.OPENWEATHERMAP_API_KEY

#helper functions
def parse_weather_response(data):
    weather_condition = data['weather'][0]['main']
    temperature = data['main']['temp']
    
    return {'condition': weather_condition, 'temperature': temperature}


def make_weather_api_request(url):
    response = requests.get(url)
    
    return response.json()


#main functions
def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city}'
    data = make_weather_api_request(url)
    
    return parse_weather_response(data)


def get_weather_data_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    data = make_weather_api_request(url)
    
    return parse_weather_response(data)