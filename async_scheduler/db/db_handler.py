import asyncio
import os
from sqlalchemy import Result
from typing import Tuple, List
import aiohttp
from models.city_weather import Base, City, Weather
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


PG_USER = os.getenv('PG_USER', 'postgres')
PG_PWD = os.getenv('PG_PWD', 'nomnom')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', 5432)
PG_DB = os.getenv('PG_DB', 'postgres')
CITIES_FILENAME = os.getenv('CITIES_FILENAME', '81_largest_city.txt')

DATABASE_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


class AsyncDB:

    def __init__(self, logger) -> None:
        self.logger = logger
        self.db_engine = create_async_engine(DATABASE_URL, echo=True)
        self.async_session = async_sessionmaker(self.db_engine, expire_on_commit=False)

    def city_generator(self) -> list:
        with open(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), CITIES_FILENAME)) as f:
            q = f.read()
        return (x for x in q.split('\n'))

    async def insert_objects(self) -> None:
        async with self.async_session() as session:
            async with session.begin():
                session.add_all(
                    [City(name=city_name) for city_name in self.city_generator()]
                )

    async def fill_db_w_initial_data(self) -> None:
        # создаёт таблицы со структурой из моделей алхимии
        async with self.db_engine.begin() as db_conn:
            await db_conn.run_sync(Base.metadata.create_all)

        # наполняет таблицу Cities городами из файла
        await self.insert_objects()
        self.logger.info("DB init done.")

    async def get_cities_list(self) -> Result[Tuple[City]]:
        async with self.async_session() as session:
            return await session.execute(select(City))
        #await session.commit()
        #return res

    async def update_cities_weather(self, cities_weather: List[dict]):
        #for city_dict in cities_weather:

        #self.session.add(Weather(city_id=city.id, **r['weather']))
        pass


# async def fetch_weather(aiohttp_session, session, city, url):
#     async with aiohttp_session.get(url) as resp:
#         r = await resp.json()
#     session.add(Weather(city_id=city.id, **r['weather']))


# async def select_and_update_objects(
#     async_session: async_sessionmaker[AsyncSession],
# ) -> None:
#     async with async_session() as session:
#         stmt = select(City)

#         result = await session.execute(stmt)

#         api_url = 'http://weather_api:5000/weather/'

#         tasks = []
#         async with aiohttp.ClientSession() as aiohttp_session:
#             for city in result.scalars():
#                 task = fetch_weather(aiohttp_session, session, city, f'{api_url}{city.name}')
#                 tasks.append(asyncio.ensure_future(task))

#             await asyncio.gather(*tasks)

#         await session.commit()


# async def async_main() -> None:
#     db_engine = create_async_engine(DATABASE_URL, echo=True)

#     async_session = async_sessionmaker(db_engine, expire_on_commit=False)

#     async with db_engine.begin() as db_conn:
#         await db_conn.run_sync(Base.metadata.create_all)

#     await insert_objects(async_session)
#     logger.info("DB init done.")

#     logger.info(f"Update loop with period of {UPDATE_TIMER} seconds started.")
#     while True:
#         await asyncio.sleep(UPDATE_TIMER)
#         await select_and_update_objects(async_session)
#         logger.info("Weather update done.")

#asyncio.run(async_main())
