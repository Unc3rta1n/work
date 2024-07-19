import requests
import logging
from utils.setting import get_config
from database.models import *
from sqlalchemy.orm import sessionmaker
import requests

config = get_config()
api_token = config["OpenWeather"]["api_token"]


Sessionlocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class WeatherParser:
    """Класс для получения погоды с API openweathermap"""
    def __init__(self, city_name=None):
        self.url = "http://api.openweathermap.org/data/2.5/weather"
        # возможно стоит поменять сайт, то связь отрубает,
        # то таймаут эррор падает
        self.params = {
            'q': city_name,
            'appid': api_token,
            'units': 'metric',
            'lang': 'ru'
        }
        self.weather_info = {}

    def parse(self):
        try:

            logging.info("Парсим город")
            response = requests.get(self.url, self.params)
            # (response.json())
            data = response.json()
            main = data['main']
            wind = data['wind']
            weather_description = data['weather'][0]['description']

            weather_info = {
                'temperature': main['temp'],
                'pressure': main['pressure'],
                'humidity': main['humidity'],
                'wind_speed': wind['speed'],
                'description': weather_description
            }
            print(weather_info)
            # todo: необходимо записывать погоду и тп в какие то поля, может прям в этом классе завести
        except Exception as e:
            logging.error(f"Exception: {e}")

    def save_data(self):
        pass
        # todo: здесь надо закидывать в базу данных информацию о погоде



