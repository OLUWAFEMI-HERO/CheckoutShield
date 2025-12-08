import os

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://checkoutshield:checkoutshield@localhost:5432/checkoutshield",
)


engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


SessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)