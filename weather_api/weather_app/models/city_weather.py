from pydantic import BaseModel


class Weather(BaseModel):
    temperature: int
    humidity: int
    overcast: str
    wind_speed: int


class CityWeather(BaseModel):
    city_name: str
    weather: Weather
