import requests
from django.forms import ModelForm, TextInput
from .models import City
from django.core.exceptions import ValidationError

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

    def clean_name(self):
        city = City.objects.filter(name=self.cleaned_data.get('name').capitalize()).count()
        if city:
            raise ValidationError('City already registered')
        url = "https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6ccee1891e64b258629ef5942ff1d522"
        r = requests.get(url.format(self.cleaned_data.get('name')))
        if not r.ok:
            raise ValidationError("City not found")
        return self.cleaned_data.get('name').capitalize()
