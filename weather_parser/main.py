import uvicorn
from fastapi_weather.fastapi import *


uvicorn.run(app, host="127.0.0.1", port=8001)  # прикол для дебага
