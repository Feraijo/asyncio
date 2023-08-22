import asyncio
import logging
import os

from db.db_handler import AsyncDB
from api.api_handler import WeatherAPI

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

UPDATE_TIMER = int(os.getenv('UPDATE_TIMER', '5'))


async def async_main() -> None:

    # init DB handler
    db = AsyncDB(logger)
    await db.fill_db_w_initial_data()

    # init API handler
    api = WeatherAPI()

    logger.info(f"Update loop with period of {UPDATE_TIMER} seconds started.")
    while True:
        await asyncio.sleep(UPDATE_TIMER)
        cities_list = await db.get_cities_list()
        cities_weather = await api.get_cities_weather(cities_list)
        await db.update_cities_weather(cities_weather)

asyncio.run(async_main())