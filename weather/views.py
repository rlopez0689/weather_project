import requests
from django.shortcuts import render
from django.core.cache import cache

from django.core.paginator import Paginator
from django.conf import settings

from .models import City
from .forms import CityForm


def index(request):

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
            form = CityForm()
    
    else:
        form = CityForm()

    weather_data = []
    cities = City.objects.all().order_by('-created_at') if all else City.objects.all().order_by('-created_at')
    paginator = Paginator(cities, 3)
    page = request.GET.get('page', 1)
    cities = paginator.get_page(page)
    for city in cities:
        city_weather = cache.get(city.name.replace(" ", ""))
        if not city_weather:
            r = requests.get(settings.WEATHER_API.format(city, settings.WEATHER_API_KEY)).json()
            city_weather = {
                'city': city.name,
                'temperature': r['main']['temp'],
                'description': r['weather'][0]['description'],
                'icon': r['weather'][0]['icon']
            }
            cache.set(city.name.replace(" ", ""), city_weather, settings.CACHE_TIME)
        weather_data.append(city_weather)
    context = {'weather_data': weather_data, 'form': form, 'cities': cities,
               'pages': range(1, cities.paginator.num_pages+1)}
    return render(request, 'index.html', context)


