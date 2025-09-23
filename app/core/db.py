from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.database_url, echo=False)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with async_session_maker() as session:
        yield session


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime, nullable=True)
