import uvicorn
from fastapi import FastAPI
from weather_app.core.config import settings
from weather_app.routers.weather import router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("asgi:app", host="127.0.0.1", port=5000,
                log_level=settings.LOG_LEVEL, reload=True)
