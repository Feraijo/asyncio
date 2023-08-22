import os
import asyncio
from typing import Tuple, List
from sqlalchemy import Result
from models.city_weather import Base, City, Weather
import aiohttp

API_URL = os.getenv('API_URL', 'weather_api')
API_PORT = os.getenv('API_PORT', '5000')

class WeatherAPI():

    def __init__(self) -> None:
        self.api_url = f'http://{API_URL}:{API_PORT}/weather/'

    async def get_cities_weather(self, cities_list: Result[Tuple[City]]) -> List[dict]:
        async with aiohttp.ClientSession() as aiohttp_session:
            tasks = []
            for city in cities_list.scalars():
                task = await self.fetch_weather(aiohttp_session, f'{self.api_url}{city.name}', city.id)
                tasks.append(asyncio.ensure_future(task))

            return await asyncio.gather(*tasks)

    async def fetch_weather(self, aiohttp_session, url, city_id):
        async with aiohttp_session.get(url) as resp:
            #r = await resp.json()
            return await resp.json()#.update({'city_id':city_id})
        #session.add(Weather(city_id=city.id, **r['weather']))

