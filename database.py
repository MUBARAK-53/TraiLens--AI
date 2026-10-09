from sqlalchemy.ext.asyncio import async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL="postgresql+asyncpg://postgres:Audix%402028@localhost:5432/TraiLens"

engine=create_async_engine(url=DATABASE_URL,echo=True)

AsyncSessionLocal=async_sessionmaker(bind=engine,expire_on_commit=False)


class Base(DeclarativeBase):
    pass