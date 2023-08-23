from fastapi import APIRouter
from weather_app.controllers.city_weather_controller import \
    CityWeatherController
from weather_app.models.city_weather import CityWeather

router = APIRouter()


@router.get("/")
async def usage():
    return [{"Usage": "/weather/<city name>"}]


@router.get("/weather/{city_name}")
async def get_city_weather(city_name: str) -> CityWeather:
    return await CityWeatherController.create(city_name)
