from fastapi import FastAPI
from parser.parser import *
from typing import Optional
app = FastAPI(title="Weather Parsing")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/weather/view", response_model=DefaultResponse)
async def view_weather(city_name: str) -> DefaultResponse:
    """Роут для вывода погоды в определенном городе"""
    response = await get_weather_from_db(city_name)
    return response


@app.delete("/weather/delete", response_model=DefaultResponse)
async def delete_city(city_name: str) -> DefaultResponse:
    """Роут для удаления города из отслеживания"""
    response = await remove_city_from_parsing(city_name)
    return response


@app.post("/weather/add", response_model=DefaultResponse)
async def add_city(city_name: str) -> DefaultResponse:
    """Роут для добавления города в отслеживание"""
    response = await add_city_to_parsing(city_name)
    return response


@app.get("/weather/view_all", response_model=DefaultResponse)
async def view_all_weather():
    """Роут для вывода всей погоды из базы данных"""
    response = await get_all_weather_from_db()
    return response


@app.get("/weather/search", response_model=DefaultResponse)
async def search(city_name: str,
                 start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                 limit: Optional[int] = None, offset: Optional[int] = None):
    """Роут с необязательными параметрами"""
    response = await search_data(city_name, start_time, end_time, limit, offset)
    return response
