import requests
from django.shortcuts import render
from django.core.cache import cache
from Crypto.Cipher import AES
import base64

from django.conf import settings

from .models import City
from .forms import CityForm


def index(request):
    KEY = 'CA6A1A3A99A9BA95D3B32A4E43132A8C' 

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            form = CityForm()
    
    else:
        form = CityForm()

    weather_data = []
    cities = City.objects.all()
    for city in cities:
        cache_time = 300
        cipher = AES.new(KEY, AES.MODE_ECB)
        cache_key = base64.b64encode(cipher.encrypt(city.name.rjust(32)))
        city_weather = cache.get(cache_key)
        if not city_weather:
            r = requests.get(settings.WEATHER_API.format(city, settings.WEATHER_API_KEY)).json()
            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']
            }
            cache.set(cache_key, city_weather, cache_time)
        else:
            print("Value cached ", city)
        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', context)


