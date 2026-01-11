from fastapi import FastAPI
from .apps.example import routes as example

app = FastAPI()

app.include_router(example.router)
