import uvicorn
from fastapi_weather.fastapi import *
import asyncio


async def parse_data():
    """Запускаем парсер каждый час."""
    logging.info("Сбор информации с городов")
    while True:
        await get_data_for_all_cities()
        await asyncio.sleep(3600)


# Запуск периодической проверки в event loop
loop = asyncio.get_event_loop()
loop.create_task(parse_data())


# uvicorn.run(app, host="127.0.0.1", port=8001)  # прикол для дебага
