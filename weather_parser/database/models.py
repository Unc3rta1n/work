from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.setting import get_config


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


config = get_config()
db_user = config["SQLAlchemy"]["db_user"]
db_pass = config["SQLAlchemy"]["db_pass"]
db_name = config["SQLAlchemy"]["db_name"]
db_host = config["SQLAlchemy"]["db_host"]
db_port = config["SQLAlchemy"]["db_port"]

connection_string = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
engine = create_engine(connection_string, echo=False)
Base.metadata.create_all(bind=engine)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

