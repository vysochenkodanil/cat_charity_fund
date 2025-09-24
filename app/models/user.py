from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
