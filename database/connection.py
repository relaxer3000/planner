from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager

from config.settings import settings
from models.users import User
from models.events import Event


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    client = AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(database=client["planner"], document_models=[User, Event])

    yield
    client.close()
