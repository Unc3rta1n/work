from pydantic import BaseModel
from typing import Optional, Any


class DefaultResponse(BaseModel):
    """Стандартный ответ от API."""
    error: bool
    message: Optional[str]
    payload: Optional[Any]


class PressureResponse(BaseModel):
    """Ответ для получения давления."""
    pressure: Optional[Any]
    id: Optional[int]
    date: Optional[Any]


class TemperatureResponse(BaseModel):
    """Ответ для получения температуры."""
    temperature: Optional[Any]
    id: Optional[int]
    date: Optional[Any]


class AllWeatherResponse(BaseModel):
    """Ответ для получения погоды."""
    weather: Optional[Any]


class AverageResponse(BaseModel):
    """Ответ для получения средней температуры."""
    temperature: Optional[Any]
    id: Optional[int]
    date: Optional[Any]