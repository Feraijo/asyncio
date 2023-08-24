import asyncio
import os
from typing import List, Tuple

import aiohttp
import requests

from models.city_weather import City

API_URL = os.getenv('API_URL', 'localhost')
API_PORT = os.getenv('API_PORT', '5000')
API_URL = f'http://{API_URL}:{API_PORT}/weather/'


async def get_cities_weather(cities_list: List[Tuple[City]]) -> List[dict]:
    async with aiohttp.ClientSession(raise_for_status=True) as aiohttp_session:
        tasks = []
        for city in cities_list:
            task = fetch_weather(aiohttp_session, f'{API_URL}{city.name}', city.id)
            tasks.append(asyncio.ensure_future(task))
        return await asyncio.gather(*tasks)


async def fetch_weather(aiohttp_session, url, city_id):
    async with aiohttp_session.get(url) as resp:
        try:
            r = await resp.json()
            r['city_id'] = city_id
            return r
        except requests.exceptions.HTTPError as e:
            return "Error: " + str(e)
