import asyncio
import os
from sqlalchemy import Result
from typing import Tuple, List
import aiohttp
from models.city_weather import Base, City, Weather
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


PG_USER = os.getenv('PG_USER', 'test')
PG_PWD = os.getenv('PG_PWD', 'test')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', 5444)
PG_DB = os.getenv('PG_DB', 'db_test')
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

    async def update_cities_weather(self, cities_weather: List[dict]):
        async with self.async_session() as session:
            for city_dict in cities_weather:
                session.add(Weather(city_id=city_dict['city_id'], **city_dict['weather']))
            await session.commit()
