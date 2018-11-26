from django.test import Client, TestCase
from urllib.parse import urlencode
from weather.models import City
from unittest.mock import patch

from django.conf import settings


class CityTestCase(TestCase):

    def test_cities_are_identified(self):
        City.objects.create(name="TestCity")
        City.objects.create(name="TestCity2")
        test_city = City.objects.get(name="TestCity")
        test_city2 = City.objects.get(name="TestCity2")
        self.assertEqual("TestCity", str(test_city), "TestCity")
        self.assertEqual("TestCity2", str(test_city2))

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    @patch("weather.forms.requests")
    def test_valid_request(self, request_form, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        request_form.get.return_value.ok.return_value = True
        cache_mock.get.return_value = None
        cache_mock.set.return_value = None
        mock_request.get.return_value.json.return_value = {'main':{'temp':'temp'},
                                                           'weather':[{'description':'',
                                                                       'icon':''}]}
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual(len(response.context['weather_data']), 1)
        self.assertEqual("Barcelona", response.context['weather_data'][0]['city'])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    @patch("weather.forms.requests")
    def test_not_exist_city(self, request_form, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        request_form.get.return_value.ok = None
        response = client.post('/', data=urlencode({"name": "Not Exist City"}),
                               content_type='application/x-www-form-urlencoded')
        mock_request.get.assert_not_called()
        cache_mock.get.assert_not_called()
        cache_mock.set.assert_not_called()
        self.assertEqual("City not found", response.context['form'].errors['name'][0])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    @patch("weather.forms.requests")
    def test_duplicate_city(self, request_form, mock_request, cache_mock):
        City.objects.all().delete()
        City.objects.create(name="Barcelona")
        client = Client()
        cache_mock.set.return_value = None
        cache_mock.get.return_value = None
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        request_form.get.assert_not_called()
        self.assertEqual("City already registered", response.context['form'].errors['name'][0])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    @patch("weather.forms.requests")
    def test_cache_city(self, request_form, mock_request, cache_mock):
        City.objects.all().delete()
        City.objects.create(name="Barcelona")
        cache_mock.set.return_value = "City"
        cache_mock.get.return_value({"city": "Barcelona",
                                     "temperature":"2",
                                     "description":"hey", "icon": "ehey"})
        client = Client()
        client.get('/')
        request_form.get.assert_not_called()
        mock_request.assert_not_called()

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    @patch("weather.forms.requests")
    def test_not_cache_city(self, request_form, mock_request, cache_mock):
        city = "Barcelona"
        City.objects.all().delete()
        client = Client()
        cache_mock.get.return_value = None
        cache_mock.set.return_value = None
        request_form.get.return_value.ok = True
        client.post('/', data=urlencode({"name": city}),
                    content_type='application/x-www-form-urlencoded')
        url = settings.WEATHER_API
        mock_request.get.assert_called_once_with(url.format(city,
                                                            settings.WEATHER_API_KEY))
