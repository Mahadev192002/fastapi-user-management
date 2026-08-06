from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config import settings

# SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"


# Create an asynchronous SQLAlchemy engine using the database URL from the settings
engine = create_async_engine( settings.database_url)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass


async def get_db(): # Define an asynchronous generator function to provide a database session for dependency injection in FastAPI routes
    async with AsyncSessionLocal() as session: # Create an asynchronous context manager to manage the lifecycle of the database session
        yield session # Yield the session to the caller, allowing it to be used in FastAPI route handlers, and automatically close the session when done