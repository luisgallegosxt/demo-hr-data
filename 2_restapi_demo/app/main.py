from fastapi import FastAPI
from core.db import Base, engine
from api.main import api_router
from core.config import settings
from core.db import SessionLocal
from utils import init_db

app = FastAPI(
    title = "Globant db migration demo" 
)

def init_app():
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

# Initialize the database on startup
init_app()

app.include_router(api_router, prefix=settings.API_V1_STR)



