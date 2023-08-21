import asyncio
import logging
import os

import aiohttp
from models.city_weather import Base, City, Weather
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


UPDATE_TIMER = int(os.getenv('UPDATE_TIMER'))

PG_USER = os.getenv('PG_USER')
PG_PWD = os.getenv('PG_PWD')
PG_HOST = os.getenv('PG_HOST')
PG_PORT = os.getenv('PG_PORT')
PG_DB = os.getenv('PG_DB')

DATABASE_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


def get_city_gen() -> list:
    with open(os.path.join(os.path.dirname(__file__), '81_largest_city.txt')) as f:
        q = f.read()
    return (x for x in q.split('\n'))


async def insert_objects(async_session: async_sessionmaker[AsyncSession]) -> None:
    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [City(name=city_name) for city_name in get_city_gen()]
            )


async def fetch_weather(aiohttp_session, session, city, url):
    async with aiohttp_session.get(url) as resp:
        r = await resp.json()
    session.add(Weather(city_id=city.id, **r['weather']))


async def select_and_update_objects(
    async_session: async_sessionmaker[AsyncSession],
) -> None:
    async with async_session() as session:
        stmt = select(City)

        result = await session.execute(stmt)

        api_url = 'http://weather_api:5000/weather/'

        tasks = []
        async with aiohttp.ClientSession() as aiohttp_session:
            for city in result.scalars():
                task = fetch_weather(aiohttp_session, session, city, f'{api_url}{city.name}')
                tasks.append(asyncio.ensure_future(task))

            await asyncio.gather(*tasks)

        await session.commit()


async def async_main() -> None:
    db_engine = create_async_engine(DATABASE_URL, echo=True)

    async_session = async_sessionmaker(db_engine, expire_on_commit=False)

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.create_all)

    await insert_objects(async_session)
    logger.info("DB init done.")

    logger.info(f"Update loop with period of {UPDATE_TIMER} seconds started.")
    while True:
        await asyncio.sleep(UPDATE_TIMER)
        await select_and_update_objects(async_session)
        logger.info("Weather update done.")

asyncio.run(async_main())
