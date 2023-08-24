import os
from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

PG_USER = os.getenv('PG_USER', 'test')
PG_PWD = os.getenv('PG_PWD', 'test')
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', 5444)
PG_DB = os.getenv('PG_DB', 'db_test')

DATABASE_URL: str = f"postgresql+asyncpg://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session: Callable[[], AsyncSession] = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)
