from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.config import Config

async_engine = create_async_engine(
    url=Config.DATABASE_URL,
    echo=True
)


async def init_db():
    async with async_engine.begin() as conn:
        #from src.books.models import Book
        #await conn.run_sync(Book.metadata.create_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async_session = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
