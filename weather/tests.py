from django.test import Client, TestCase
from urllib.parse import urlencode
from weather.models import City
from unittest.mock import patch


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
    def test_valid_request(self, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        cache_mock.get.return_value = None
        cache_mock.set.return_value = None
        mock_request.get.return_value.json.return_value = {'main':{'temp':'temp'}, 'weather':[{'description':'', 'icon':''}]}
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual(len(response.context['weather_data']), 1)
        self.assertEqual("Barcelona", response.context['weather_data'][0]['city'])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    def test_not_exist_city(self, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        cache_mock.set.return_value = None
        response = client.post('/', data=urlencode({"name": "Not Exist City"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual("City not found", response.context['form'].errors['name'][0])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    def test_duplicate_city(self, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        cache_mock.set.return_value = None
        client.post('/', data=urlencode({"name": "Barcelona"}),
                    content_type='application/x-www-form-urlencoded')
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual("City already registered", response.context['form'].errors['name'][0])

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    def test_cache_city(self, mock_request, cache_mock):
        City.objects.all().delete()
        City.objects.create(name="Barcelona")
        cache_mock.set.return_value = "City"
        cache_mock.get.return_value({"city": "Barcelona", "temperature":"2", "description":"hey", "icon": "ehey"})
        client = Client()
        client.get('/')
        self.assertFalse(mock_request.called)

    @patch("weather.views.cache")
    @patch("weather.views.requests")
    def test_not_cache_city(self, mock_request, cache_mock):
        City.objects.all().delete()
        client = Client()
        cache_mock.get.return_value = None
        cache_mock.set.return_value = None
        client.post('/', data=urlencode({"name": "Barcelona"}), content_type='application/x-www-form-urlencoded')
        mock_request.get.assert_called_once_with("https://api.openweathermap.org/data/2.5/weather?q=Barcelona&units=metric&appid=6ccee1891e64b258629ef5942ff1d522")

