import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
import urllib.parse
from weatherbeats.weather_utils import get_weather_data_by_coords
from weatherbeats.spotify_utils import get_spotify_token, fetch_spotify_recommendation



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
        'scope': 'user-read-private user-read-email streaming user-read-playback-state'
    }
    url = f'https://accounts.spotify.com/authorize?{urllib.parse.urlencode(params)}'

    return redirect(url)


def spotify_callback(request):
    authorization_code = request.GET.get('code')
    access_token = get_spotify_token(authorization_code)

    print("Access Token:", access_token)
    
    request.session['spotify_access_token'] = access_token
    
    return redirect('index')


def get_weather_by_coords(request):
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    weather_data = get_weather_data_by_coords(lat, lon)
    
    return JsonResponse(weather_data)


def get_spotify_recommendation(request):
    weather_condition = request.GET.get('weatherCondition')
    access_token = request.session.get('spotify_access_token')

    print("Access Token from session:", access_token)
    
    if not access_token:
        return JsonResponse({'error': 'Access token not found'}, status=401)
    
    song_data = fetch_spotify_recommendation(weather_condition, access_token)
    
    return JsonResponse(song_data)



def results(request):
    weather_json = request.GET.get('weather')
    song_json = request.GET.get('song')
    authorization_code = request.GET.get('code')
    spotify_access_token = get_spotify_token(authorization_code)

    if weather_json and song_json:
        weather_data = json.loads(weather_json)
        song_data = json.loads(song_json)

        context = {
            'weather': weather_data,
            'song': song_data,
            'spotfiy_access_token': spotify_access_token
        }

        return render(request, 'results.html', context)
    else:
        return HttpResponse("Missing data", status=400)