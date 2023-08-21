import os

import yaml
from pydantic_settings import BaseSettings

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(os.path.dirname(here), 'config/local.yml')) as f:
    sett_dict = yaml.load(f, Loader=yaml.FullLoader)


class Settings(BaseSettings):
    PROJECT_NAME: str

    LOG_LEVEL: str

    POSTGRES_SERVER: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @property
    def CONN_STRING(self) -> str:
        return "{drivername}://{user}:{password}@{server}:{port}/{database}".format(
            drivername="postgresql+asyncpg",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            server=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            database=self.POSTGRES_DB,
        )


settings = Settings(**sett_dict)
