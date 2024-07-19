import utils
from database.models import init_database
from parser.parser import WeatherParser

init_database()

wp = WeatherParser(city_name='Челябинск')
wp.parse()
