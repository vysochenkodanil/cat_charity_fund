from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    comment: Optional[str] = None
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


# Схема для обычного пользователя (ограниченные поля)
class DonationUserDB(BaseModel):
    id: int
    comment: Optional[str] = None
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True
