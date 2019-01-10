# Weather Project Django App

This is a simple Weather App made on Django that queries the WeatherApi for the actual weather of a city. 

![Weather Screen](https://s3.amazonaws.com/myimagesrl/WeatherScreen.png)

## SetUp
There are some env variables needed in order to work:
* WEATHER_API_KEY = YOUR_WEATHER_API_KEY
* SECRET_KEY = YOUR_SECRET_DJANGO_KEY

For the database:
* DB_ENGINE
* DB_NAME
* DB_USER
* DB_PASSWORD
* DB_HOST
* PORT

For Cache(default is memcache):
* CACHE_URL

Or having a localsettings file:
```
SECRET_KEY = 'YOUR DJANGO SECRETKEY'
DEBUG = True

WEATHER_API_KEY = "YOURAPIKEY"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'localhost:11211',
    }
}
```

## Building

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py runserver
```

Then visit `http://localhost:8000` to view the app.
