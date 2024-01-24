import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
import urllib.parse
from weatherbeats.weather_utils import get_weather_data, get_weather_data_by_coords
from weatherbeats.spotify_utils import get_spotify_recommendations



def oauth(request):
    return render(request, 'weatherbeats/oauth.html')


def index(request):
    return render(request, 'weatherbeats/index.html')


def results(request):
    return render(request, 'weatherbeats/results.html')


def spotify_connect(request):
    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'scope': 'user-read-private user-read-email'
    }
    url = f'https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}'

    return redirect(url)


def get_weather_by_zipcode(request, zipcode):
    api_key = settings.OPENWEATHERMAP_API_KEY
    url = f'https://api.openweathermap.org/data/2.5/weather?zip={zipcode}&appid={api_key}'
    response = requests.get(url)

    return JsonResponse(response.json())


def get_weather_by_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    weather_data = get_weather_data_by_coords(lat, lon)
    
    return JsonResponse(weather_data)


def get_spotify_recommendation(request):
    weather_condition = request.GET.get('weatherCondition')
    song_data = get_spotify_recommendations(weather_condition)
    
    return JsonResponse(song_data)


def results(request):
    weather_json = request.GET.get('weather')
    song_json = request.GET.get('song')

    if weather_json and song_json:
        weather_data = json.loads(weather_json)
        song_data = json.loads(song_json)

        context = {
            'weather': weather_data,
            'song': song_data
        }

        return render(request, 'results.html', context)
    else:
        return HttpResponse("Missing data", status=400)