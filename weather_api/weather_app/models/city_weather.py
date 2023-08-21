import asyncio

from pydantic import BaseModel
from weather_app.utility.weather_randomizer import get_city_weather


class Weather(BaseModel):
    temperature: int
    humidity: int
    overcast: str
    wind_speed: int


class CityWeather(BaseModel):
    city_name: str
    weather: Weather

    @classmethod
    async def create(cls, city_name):
        await asyncio.sleep(2)  # imitate api call
        self = CityWeather(city_name=city_name, weather=get_city_weather(city_name))
        return self
