import asyncio
import logging
import os

from api.api_client import get_cities_weather
from db.db_client import (fill_db_w_initial_data, get_cities_result,
                          update_cities_weather)

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
    await fill_db_w_initial_data()
    logger.info("DB init done.")

    logger.info(f"Update loop with period of {UPDATE_TIMER} seconds started.")
    while True:
        await asyncio.sleep(UPDATE_TIMER)
        cities_result = await get_cities_result()
        cities_weather = await get_cities_weather(cities_result.scalars())
        await update_cities_weather(cities_weather)

asyncio.run(async_main())
