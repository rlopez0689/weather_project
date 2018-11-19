from django.test import Client, TestCase
from urllib.parse import urlencode
from weather.models import City
from unittest.mock import patch


class CityTestCase(TestCase):

    def test_cities_are_identified(self):
        """Cities are correctly identified"""
        City.objects.create(name="TestCity")
        City.objects.create(name="TestCity2")
        test_city = City.objects.get(name="TestCity")
        test_city2 = City.objects.get(name="TestCity2")
        self.assertEqual("TestCity", str(test_city), "TestCity")
        self.assertEqual("TestCity2", str(test_city2))

    def test_valid_request(self):
        City.objects.all().delete()
        client = Client()
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual(len(response.context['weather_data']), 1)
        self.assertEqual("Barcelona", response.context['weather_data'][0]['city'])

    def test_not_exist_city(self):
        City.objects.all().delete()
        client = Client()
        response = client.post('/', data=urlencode({"name": "Not Exist City"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual("City not found", response.context['form'].errors['name'][0])

    def test_duplicate_city(self):
        City.objects.all().delete()
        client = Client()
        client.post('/', data=urlencode({"name": "Barcelona"}),
                    content_type='application/x-www-form-urlencoded')
        response = client.post('/', data=urlencode({"name": "Barcelona"}),
                               content_type='application/x-www-form-urlencoded')
        self.assertEqual("City already registered", response.context['form'].errors['name'][0])

    @patch("django.core.cache.cache.get")
    @patch("requests.get")
    def test_cache_city(self, mock_request, cache_mock):
        City.objects.all().delete()
        City.objects.create(name="Barcelona")
        cache_mock.return_value({"city": "Barcelona", "temperature":"2", "description":"hey", "icon": "ehey"})
        client = Client()
        client.get('/')
        self.assertFalse(mock_request.called)

    @patch("requests.get")
    def test_not_cache_city(self, mock_request):
        City.objects.all().delete()
        client = Client()
        client.post('/', data=urlencode({"name": "Barcelona"}), content_type='application/x-www-form-urlencoded')
        mock_request.assert_called_once_with("https://api.openweathermap.org/data/2.5/weather?q=Barcelona&units=metric&appid=6ccee1891e64b258629ef5942ff1d522")

