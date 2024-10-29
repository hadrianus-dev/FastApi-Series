from sqlalchemy import text
from sqlmodel import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from uvicorn import Config
from src.config import Config

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True
    )
)

async def init_db():
    async with engine.begin() as conn:
        statement = text("SELECT 'hallo';")
        reuslt = await conn.execute(statement)

        print(reuslt.all())
