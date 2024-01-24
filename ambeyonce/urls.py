"""
URL configuration for ambeyonce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weatherbeats import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.oauth, name='oauth'),
    path('index', views.index, name='index'),
    path('results', views.results, name='results'),
    path('spotify-connect/', views.spotify_connect, name='spotify_connect'),
    path('get-weather/<str:zipcode>', views.get_weather_by_zipcode, name='get_weather_by_zipcode'),
    path('get-weather-by-coords/', views.get_weather_by_coords, name='get_weather_by_coords'),
    path('get-spotify-recommendation/', views.get_spotify_recommendation, name='get_spotify_recommendation'),
]