import requests

from django.forms import ModelForm, TextInput
from django.core.exceptions import ValidationError
from django.conf import settings

from .models import City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

    def clean_name(self):
        city = City.objects.filter(name=self.cleaned_data.get('name').capitalize()).count()
        if city:
            raise ValidationError('City already registered')
        url = settings.WEATHER_API
        req = requests.get(url.format(self.cleaned_data.get('name'), settings.WEATHER_API_KEY))
        if not req.ok:
            raise ValidationError("City not found")
        return self.cleaned_data.get('name').capitalize()
