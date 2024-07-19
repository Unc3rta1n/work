import requests
import logging
from utils.setting import get_config

config = get_config()
api_token = config["OpenWeather"]["api_token"]


class WeatherParser:
    def __init__(self, city_name=None):
        self.url = "http://api.openweathermap.org/data/2.5/weather"
        self.params = {
            'q': city_name,
            'appid': api_token,
            'units': 'metric',
            'lang': 'ru'
        }

    def parse(self):
        try:
            logging.info("Парсим город")
            response = requests.get(self.url, self.params)
            print(response.json())
        except Exception as e:
            logging.error(f"Exception: {e}")
