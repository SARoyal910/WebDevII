from backend.app.routers import auth, protected


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
#from backend import app

app = FastAPI()

# CORS (adjust origins as needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
# include both routers defined in protected.py
app.include_router(protected.admin_router)
app.include_router(protected.protected_router)

# Routers
app.include_router(auth.router)
app.include_router(protected.router)

# DB (adjust config to your models/module)
register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["backend.app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

