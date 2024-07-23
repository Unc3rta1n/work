import logging
import requests

from database.models import *
from datetime import datetime, timedelta
from database.models import Sessionlocal
from fastapi_weather.schemas import *

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


async def save_data(weather_data: dict, city_name: str):
    try:
        with Sessionlocal() as db:
            weather = Weather(
                temperature=weather_data["temperature"],
                pressure=weather_data["pressure"],
                humidity=weather_data["humidity"],
                wind=weather_data["wind"],
                feeling=weather_data["feeling"],
                date=datetime.now()
            )
            logging.info("Сохраняем информацию о погоде в БД")
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


async def get_data_for_all_cities():
    try:
        with Sessionlocal() as db:
            cities = db.query(City).all()
            for city in cities:
                logging.info(city.city_name)
                weather = WeatherParser(city_name=city.city_name)
                data = weather.parse()
                await save_data(data, city.city_name)
    except Exception as e:
        logging.error(f"Exception:{e}")


async def get_weather_from_db(city_name: str) -> DefaultResponse:
    logging.info(f'Ищем город {city_name} в базе данных')
    result = []
    try:
        with Sessionlocal() as db:
            city = db.query(City).filter_by(city_name=city_name).first()
            if city:
                city_weathers = db.query(CityWeather).filter_by(city_id=city.id).all()
                for city_weather in city_weathers:
                    weather = db.query(Weather).filter_by(id=city_weather.weather_id).first()
                    weather_data = {"id": weather.id,
                                    "temperature": weather.temperature,
                                    "pressure": weather.pressure,
                                    "humidity": weather.humidity,
                                    "wind": weather.wind,
                                    "feeling": weather.feeling,
                                    "date": weather.date.strftime("%Y-%m-%d")
                                    }
                    result.append(weather_data)

                if len(result):
                    response = DefaultResponse(error=False, message="Ok",
                                               payload=AllWeatherResponse(weather=result))
                    return response
            else:
                logging.info(f"Город {city_name} не найден в базе данных")
                return DefaultResponse(error=True, message='Город не найден в базе данных', payload=None)

    except Exception as e:
        logging.error(f'Произошла ошибка при поиске/вытягивании данных из базы данных: {e}')


async def get_all_weather_from_db() -> DefaultResponse:
    logging.info('Собираем всю погоду с базы данных')
    result = []
    try:
        with Sessionlocal() as db:
            cities = db.query(City).all()
            for city in cities:
                city_weathers = db.query(CityWeather).filter_by(city_id=city.id).all()
                result.append({"city": city.city_name})
                for city_weather in city_weathers:
                    weather = db.query(Weather).filter_by(id=city_weather.weather_id).first()
                    weather_data = {"id": weather.id,
                                    "temperature": weather.temperature,
                                    "pressure": weather.pressure,
                                    "humidity": weather.humidity,
                                    "wind": weather.wind,
                                    "feeling": weather.feeling,
                                    "date": weather.date.strftime("%Y-%m-%d")
                                    }
                    result.append(weather_data)

        if len(result):
            response = DefaultResponse(error=False, message="Ok",
                                       payload=AllWeatherResponse(weather=result))
            return response

    except Exception as e:
        logging.error(f"Произошла ошибка при выводе всей погоды: {e}")
        return DefaultResponse(error=True, message="Not Ok", payload=None)


async def add_city_to_parsing(city_name: str) -> DefaultResponse:
    try:
        logging.info(f"Добавляем город {city_name} в БД")
        with Sessionlocal() as db:
            city = City(city_name=city_name)
            db.add(city)
            db.commit()
            return DefaultResponse(error=False, message='Ok', payload=None)

    except Exception as e:
        logging.error(f"Ошибка при добавлении города в базу данных, {e}")
        return DefaultResponse(error=True, message=' Not Ok', payload="Ошибка при добавлении города в базу данных")


async def remove_city_from_parsing(city_name: str) -> DefaultResponse:
    logging.info(f"удаляем город {city_name} из БД")
    try:
        with Sessionlocal() as db:
            city = db.query(City).filter_by(city_name=city_name).first()
            if city:
                city_weathers = db.query(CityWeather).filter_by(city_id=city.id).all()
                for city_weather in city_weathers:
                    weather = db.query(Weather).filter_by(id=city_weather.weather_id).first()
                    if weather:
                        db.delete(weather)
                    db.delete(city_weather)
                db.delete(city)
                db.commit()
                return DefaultResponse(error=False, message='OK', payload=None)
            else:
                logging.warning(f"Город {city_name} не найден в базе данных")
                return DefaultResponse(error=True, message='NOT OK',
                                       payload=f"Город {city_name} не найден в базе данных")

    except Exception as e:
        logging.error(f"Ошибка при удалении города из базы данных, {e}")


async def search_data(
        city_name: str,
        start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
        limit: Optional[int] = None, offset: Optional[int] = None
) -> DefaultResponse:
    logging.info(f"Собираем информацию по городу {city_name} с необязательными параметрами")

    # Устанавливаем значения по умолчанию
    if start_time is None:
        # start_time = datetime.combine(datetime.today() - timedelta(days=1), datetime.min.time())
        start_time = datetime.combine(datetime.today(), datetime.min.time())

    if end_time is None:
        end_time = datetime.combine(datetime.today() + timedelta(days=1), datetime.min.time())
    if limit is None:
        limit = 10
    if offset is None:
        offset = 0

    result = []
    try:
        with Sessionlocal() as db:

            if city_name:
                city = db.query(City).filter_by(city_name=city_name).first()
                if city:
                    # Запрос с фильтрацией по дате и пагинацией
                    city_weathers = (
                        db.query(CityWeather)
                        .join(Weather, CityWeather.weather_id == Weather.id)
                        .filter(
                            CityWeather.city_id == city.id,
                            Weather.date >= start_time,
                            Weather.date <= end_time
                        )
                        .limit(limit)
                        .offset(offset)
                        .all()
                    )

                    for city_weather in city_weathers:
                        weather = db.query(Weather).filter_by(id=city_weather.weather_id).first()
                        weather_data = {
                            "id": weather.id,
                            "temperature": weather.temperature,
                            "pressure": weather.pressure,
                            "humidity": weather.humidity,
                            "wind": weather.wind,
                            "feeling": weather.feeling,
                            "date": weather.date.strftime("%Y-%m-%d")
                        }
                        result.append(weather_data)

                else:
                    logging.info(f"Город {city_name} не найден в базе данных")
                    return DefaultResponse(error=True, message='Город не найден в базе данных', payload=None)

            else:
                logging.info("Имя города не указано")
                return DefaultResponse(error=True, message='Имя города обязательно', payload=None)

            # Возвращаем отфильтрованный результат с учетом limit и offset
            return DefaultResponse(error=False, message='Успешно', payload=result)

    except Exception as e:
        logging.error(f"Ошибка при сборе информации по городу {city_name} : {e}")
        return DefaultResponse(error=True, message="Проверьте введенные параметры", payload=None)
