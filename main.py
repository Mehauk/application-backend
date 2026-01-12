from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

### import routes start
from .apps.example import routes as example
### import routes end

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

### routers start
app.include_router(example.router)
### routers end
