from fastapi import APIRouter
from weather_app.models.city_weather import CityWeather

router = APIRouter()


@router.get("/weather/")
async def usage():
    return [{"Usage": "/weather/<city name>"}]


@router.get("/weather/{city_name}")
async def get_city_weather(city_name: str) -> CityWeather:
    return await CityWeather.create(city_name)
