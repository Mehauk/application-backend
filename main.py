from fastapi import FastAPI

from .services.database import init_db
from .apps.example import routes as example

app = FastAPI()

app.include_router(example.router)


@app.on_event("startup")
async def on_startup():
    await init_db()
