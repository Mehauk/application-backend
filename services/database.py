from sqlmodel import SQLModel, create_engine
from ..config.database import DatabaseSettings
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

engine = AsyncEngine(
    create_engine(DatabaseSettings().database_url, echo=True, future=True),
)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session
