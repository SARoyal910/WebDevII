import os
from fastapi import FastAPI
from typing import Any
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from backend.lifespan import keiser_lifespan



DATABASE_URL: str = "postgres://postgres:postgres@localhost:5432/mydb"
REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
SESSION_COOKIE: str = "sid"
SESSION_TTL_SECONDS: int = 60*60*24*7
CORS_ORIGINS: list[Any] = ["http://localhost:5371"]
SECRET_KEY: str = "dev-secret"  # use env var in prod

app = FastAPI(lifespan=keiser_lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,        # Required for cookies across origins
    allow_methods=["*"],
    allow_headers=["*"],
)
