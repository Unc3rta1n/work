import utils
from parser.parser import WeatherParser
from parser.parser import get_data_for_all_cities, add_city_to_parsing, remove_city_from_parsing

# wp = WeatherParser(city_name='Chelyabinsk')
# wp.parse()
add_city_to_parsing("Ufa")
add_city_to_parsing("Moscow")
get_data_for_all_cities()
# remove_city_from_parsing("Moscow") - проверено, удаляет и за собой уносит все связи в таблице
# remove_city_from_parsing("Ufa")

