from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import date


class Base(DeclarativeBase):
    pass


class City(Base):
    """Класс-таблица для городов"""
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)


class Weather(Base):
    """Класс-таблица для погоды"""
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(String)
    pressure = Column(String)
    humidity = Column(String)
    wind = Column(String)
    feeling = Column(String)
    date = Column(Date, default=date.today)


class CityWeather(Base):
    """Класс-таблица, создающая связь между городами и погодой"""
    __tablename__ = "city_weather"
    city_id = Column(Integer, ForeignKey('city.id'), primary_key=True)
    weather_id = Column(Integer, ForeignKey('weather.id'), primary_key=True)
    weathers = relationship('Weather')
    cities = relationship('City')


def init_tables():
    """Функция для подключения к базе"""
    Base.metadata.create_all(bind=engine)
