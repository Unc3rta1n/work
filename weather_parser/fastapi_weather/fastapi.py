from fastapi import FastAPI
from fastapi_weather.schemas import *
from parser.parser import *
app = FastAPI(title="Weather Parsing")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/weather/view", response_model=DefaultResponse)
async def view_weather(city_name: str) -> DefaultResponse:
    response = await get_weather_from_db(city_name)
    return response


@app.delete("/weather/delete", response_model=DefaultResponse)
async def delete_city(city_name: str) -> DefaultResponse:
    response = await remove_city_from_parsing(city_name)
    return response


@app.post("/weather/add", response_model=DefaultResponse)
async def add_city(city_name: str) -> DefaultResponse:
    response = await add_city_to_parsing(city_name)
    return response

