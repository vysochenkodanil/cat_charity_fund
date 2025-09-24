from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания проекта (только обязательные поля)."""

    pass


class CharityProjectUpdate(BaseModel):
    """Схема для обновления проекта (все поля опциональные)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = "forbid"


class CharityProjectDB(CharityProjectBase):
    """Схема для возврата из API."""

    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
