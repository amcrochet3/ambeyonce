import requests
import json
from django.conf import settings
import random



#global variables
artist_id = '6vWDO969PvNqNYHIOW5v0m' #Beyonce's Spotify ID!


def get_spotify_weather_params(weather_condition):
    with open('data/spotifyWeatherParams.json', 'r') as file:
        weather_params = json.load(file)

    return weather_params.get(weather_condition, weather_params.get("Default"))


def get_spotify_token(authorization_code):
    auth_url = 'https://accounts.spotify.com/api/token'
    payload = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    }
    auth_response = requests.post(auth_url, data=payload)
    auth_response_data = auth_response.json()

    return auth_response_data.get('access_token')


def fetch_spotify_recommendation(weather_condition, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    params = get_spotify_weather_params(weather_condition)
    params['seed_artists'] = artist_id
    params['limit'] = 1
    response = requests.get('https://api.spotify.com/v1/recommendations', headers=headers, params=params)
    data = response.json()

    if data['tracks']:
        track = random.choice(data['tracks'])
        song_details = {
            'id': track['id'],
            'title': track['name'],
            'artist': ','.join(artist['name'] for artist in track['artists']),
            'album': track['album']['name'] if 'album' in track else 'N/A',
            'release_year': track['album']['release_date'][:4] if 'album' in track else 'N/A'
        }
        return song_details
    else:
        return None
