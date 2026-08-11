# conftest used for setting up fixtures for testing the FastAPI application with pytest and anyio.
# It includes fixtures for database setup, AWS S3 mocking, and HTTP client configuration.

import os
from collections.abc import AsyncGenerator

import asyncio

if hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

os.environ["DATABASE_URL"] = (
    "postgresql+psycopg://postgres:Root@localhost/test_blog"
)
os.environ["S3_BUCKET_NAME"] = "test-bucket"
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"

os.environ["S3_ACCESS_KEY_ID"] = "testing"
os.environ["S3_SECRET_ACCESS_KEY"] = "testing"
os.environ["S3_REGION"] = "us-east-1"

os.environ["AWS_ACCESS_KEY_ID"] = "testing"
os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
 
import boto3
import pytest
from httpx import ASGITransport, AsyncClient
from moto import mock_aws
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from database import Base, get_db
from main import app

pytest_plugins = ["anyio"]

# we used this fixture to specify the backend for anyio, which is used for asynchronous testing with pytest.
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

# Test database engine fixture that creates an asynchronous SQLAlchemy engine for testing purposes.
@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(
        os.environ["DATABASE_URL"],
        poolclass=NullPool,
    )
    return engine

# Fixture to set up and tear down the test database schema before and after tests run.
@pytest.fixture(scope="session")
async def setup_database(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await test_engine.dispose()

# Fixture to provide an asynchronous database session for tests, using the test engine and ensuring proper cleanup after each test. 
@pytest.fixture
async def db_session(
    test_engine,
    setup_database,
) -> AsyncGenerator[AsyncSession]:
    conn = await test_engine.connect()
    trans = await conn.begin()

    test_async_session = async_sessionmaker(
        bind=conn,
        class_=AsyncSession,
        expire_on_commit=False,
        join_transaction_mode="create_savepoint", # This option allows the session to create a savepoint for each transaction, enabling nested transactions and ensuring that changes can be rolled back without affecting the outer transaction.
    )

    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await conn.close()

# Fixture to mock AWS S3 interactions using the moto library, allowing tests to run without actual AWS credentials or network access. It creates a mock S3 bucket for testing purposes.
@pytest.fixture
def mocked_aws():
    with mock_aws():
        s3 = boto3.client("s3", region_name="us-east-1")
        s3.create_bucket(Bucket=os.environ["S3_BUCKET_NAME"])
        yield s3

# Fixture to provide an asynchronous HTTP client for testing the FastAPI application, with dependency overrides for the database session and AWS S3 mocking. It uses the ASGITransport to interact with the FastAPI app directly without needing a running server.
@pytest.fixture
async def client(
    db_session: AsyncSession,
    mocked_aws,
) -> AsyncGenerator[AsyncClient]:

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()

