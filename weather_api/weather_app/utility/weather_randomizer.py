import datetime
import random

overcast_choices = [
    'Ясно',
    'Преимущественно ясно',
    'Частично облачно',
    'Преимущественно облачно',
    'Облачно',
    'Осадки'
]


def get_city_weather(city_name: str) -> dict:
    random.seed(city_name, datetime.datetime.now())
    temperature = random.randint(-40, 40)
    humidity = random.randint(0, 100)
    overcast = random.choice(overcast_choices)
    wind_speed = random.randint(0, 20)
    return {
        'temperature': temperature,
        'humidity': humidity,
        'overcast': overcast,
        'wind_speed': wind_speed
    }
