import os
from typing import List, Tuple

from sqlalchemy import Result, select

from db import async_session, engine
from models.city_weather import Base, City, Weather

CITIES_FILENAME = os.getenv('CITIES_FILENAME', '81_largest_city.txt')


def city_generator() -> list:
    with open(os.path.join(os.path.dirname(
            os.path.dirname(__file__)), CITIES_FILENAME)) as f:
        q = f.read()
    return (x for x in q.split('\n'))


async def fill_db_w_initial_data() -> None:
    # создаёт таблицы со структурой из моделей алхимии
    async with engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.create_all)

    # наполняет таблицу Cities городами из файла
    async with async_session() as session:
        session.add_all(
            [City(name=city_name) for city_name in city_generator()]
        )
        await session.commit()


async def get_cities_result() -> Result[Tuple[City]]:
    async with async_session() as session:
        return await session.execute(select(City))


async def update_cities_weather(cities_weather: List[dict]):
    async with async_session() as session:
        for city_dict in cities_weather:
            session.add(Weather(city_id=city_dict['city_id'], **city_dict['weather']))
        await session.commit()
