import os
import asyncpg
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.models.base_class import Base
from sqlalchemy.exc import ArgumentError

DATABASE_URL = os.getenv("DATABASE_URL", None)
AsyncSessionDB = None
engine = None


async def create_session():
    global AsyncSessionDB, engine
    if not DATABASE_URL:
        raise RuntimeError("No DATABASE_URL found.")
    try:
        engine = create_async_engine(DATABASE_URL, echo=True)
    except ArgumentError as error:
        raise RuntimeError(error)
    
    AsyncSessionDB = sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionDB() as session:
        yield session


async def ping_database():
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1;"))
    except asyncpg.exceptions.InvalidCatalogNameError as error:
        raise RuntimeError(error)
    except asyncpg.exceptions.InvalidPasswordError as error:
        raise RuntimeError(error)
    except Exception as error:

        print("Errr", type(error), "al conectar a la base de datos.")
        raise RuntimeError("Está la Base de Datos activada?")


async def init_models():
    """Drop and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    DATABASE_URL = os.getenv("DATABASE_URL", None)

    async def main():
        await create_session()
        await ping_database()

    import asyncio
    asyncio.run(main())
