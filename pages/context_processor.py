import requests
from pages.forms import WeatherCityForm


def get_temp(request):
    if request.user.is_authenticated:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'
        city = 'Las Vegas'

        cities = request.user.user_weather.all()

        weather_data = []

        for city in cities:
            r = requests.get(url.format(city)).json()

            city_weather = {
                'city': city,
                'temperature': r["main"]["temp"],
                'feels_like': r["main"]["feels_like"],
                'temp_min': r["main"]["temp_min"],
                'temp_max': r["main"]["temp_max"],
                'pressure': r["main"]["pressure"],
                'humidity': r["main"]["humidity"],
                'description': r["weather"][0]["description"],
                'icon': r["weather"][0]["icon"],
            }
            weather_data.append(city_weather)

        weather_city_form = WeatherCityForm()
        return {
            'weather_city_form': weather_city_form,
            'weather_data': weather_data
        }
    else:
        return {
            'weather_city_form': None,
            'weather_data': None
        }
