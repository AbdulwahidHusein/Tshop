# app/core/config.py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()


db_client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
database = db_client.ecommerce

class Settings:
    DB = database
    JWT_SECRET_KEY: str = "supersecretkey"  # Should be loaded from env in production
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()
