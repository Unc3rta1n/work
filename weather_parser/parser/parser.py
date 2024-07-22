import requests
import logging
from utils.setting import get_config
from database.models import *
from datetime import datetime
import requests
from database.models import Sessionlocal

config = get_config()
api_token = config["OpenWeather"]["api_token"]


class WeatherParser:
    """Класс для получения погоды с API openweathermap"""

    def __init__(self, city_name=None):
        self.url = "https://api.openweathermap.org/data/2.5/weather"

        self.params = {
            'q': city_name,
            'appid': api_token,
            'units': 'metric'
            # 'lang': 'ru'
        }
        self.weather_info = {}

    def parse(self) -> dict | None:
        try:

            logging.info("Парсим город")
            response = requests.get(self.url, self.params)
            data = response.json()

            weather_info = {
                "city": str(data['name']),
                "temperature": str(int(data['main']['temp'])),
                "pressure": str(data['main']['pressure']),
                "humidity": str(data['main']['humidity']),
                "wind": str(data['wind']['speed']),
                "feeling": str(int(data['main']['feels_like'])),
            }
            return weather_info
        except Exception as e:
            logging.error(f"Exception: {e}")
            return None


def save_data(weather_data: dict, city_name: str):
    try:
        with Sessionlocal() as db:
            weather = Weather(
                temperature=weather_data["temperature"],
                pressure=weather_data["pressure"],
                humidity=weather_data["humidity"],
                wind=weather_data["wind"],
                feeling=weather_data["feeling"],
                date=datetime.now().date()
            )
            db.add(weather)
            db.flush()
            db.refresh(weather)
            weather_id = db.query(Weather).order_by(Weather.id.desc()).first()
            print(weather_id.id)
            city_id = db.query(City).filter_by(city_name=city_name).first()
            print(city_id.id, city_id.city_name)
            city_weather = CityWeather(city_id=city_id.id, weather_id=weather_id.id)
            db.add(city_weather)
            db.commit()

    except Exception as e:
        logging.error(f"Exception: {e}")


def get_data():
    try:
        with Sessionlocal() as db:
            cities = db.query(City).all()
            for city in cities:
                weather = WeatherParser(city_name=city.city_name)
                data = weather.parse()
                save_data(data, city.city_name)
    except Exception as e:
        logging.error(f"Exception:{e}")
