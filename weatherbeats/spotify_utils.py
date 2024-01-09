import requests
import json
from django.conf import settings



#global variables
artist_id = '6vWDO969PvNqNYHIOW5v0m' #Beyonce's Spotify ID!


def get_spotify_weather_params(weather_condition):
    with open('data/spotifyWeatherParams.json', 'r') as file:
        weather_params = json.load(file)

    return weather_params.get(weather_condition, weather_params.get("Default"))


def get_spotify_token():
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    })
    auth_response_data = auth_response.json()

    return auth_response_data['access_token']


def get_spotify_recommendations(weather_condition):
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = get_spotify_weather_params(weather_condition)
    params['seed_artists'] = artist_id
    params['limit'] = 1
    response = requests.get('http://api.spotify.com/v1/recommendations', headers=headers, params=params)

    return response.json()


def test_spotify_connection():
    token = get_spotify_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}/albums', headers=headers)

    return response.json()