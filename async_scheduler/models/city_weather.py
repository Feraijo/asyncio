import datetime
from typing import List

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    weather: Mapped[List["Weather"]] = relationship(cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.name} ({self.id})"


class Weather(Base):
    __tablename__ = "weather"
    recdate: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now(), primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"), primary_key=True)
    temperature: Mapped[int]
    humidity: Mapped[int]
    overcast: Mapped[str]
    wind_speed: Mapped[int]

    def __repr__(self) -> str:
        return f"{self.recdate}: {self.temp}°C"
