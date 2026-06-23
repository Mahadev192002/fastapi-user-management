from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

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