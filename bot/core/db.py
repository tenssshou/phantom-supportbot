from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

Base = declarative_base()
engine = create_async_engine(settings.database_url, echo=False, pool_pre_ping=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
async def get_session() -> AsyncSession:
async with async_session() as s:
yield s