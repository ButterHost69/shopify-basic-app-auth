from typing import Any, Callable, TypeVar, Optional

from .settings import import_settings
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import Select
from sqlalchemy import delete

settings = import_settings()

DB_Base = declarative_base()
T = TypeVar("T")


db_engine = create_async_engine(
    url=settings.db_settings.db_async_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)


async def init_db():
    async with db_engine.begin() as conn:
        await conn.run_sync(DB_Base.metadata.create_all)


DBAsyncSession: Callable[[], AsyncSession] = async_sessionmaker(
    bind=db_engine, class_=AsyncSession, expire_on_commit=False
)

# For Depends Statements in FastAPI
# async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
#     async with DBAsyncSession() as session:
#         yield session


async def fetch_one(query: Select) -> Optional[Any]:
    async with DBAsyncSession() as session:
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def fetch_all(query: Select) -> Optional[Any]:
    async with DBAsyncSession() as session:
        result = await session.execute(query)
        return result.scalars().all()


async def create(data: T):
    async with DBAsyncSession() as session:
        async with session.begin():
            session.add(data)
            await session.flush()
            return data.id  # type: ignore


async def update(query: Select, values: dict):
    async with DBAsyncSession() as session:
        async with session.begin():
            result = await session.execute(query, values)
            return result.rowcount


async def delete_all(model_cls):
    async with DBAsyncSession() as session:
        async with session.begin():
            await session.execute(delete(model_cls))
