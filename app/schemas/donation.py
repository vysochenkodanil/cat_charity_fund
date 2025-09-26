from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationBase(BaseModel):
    """Базовая модель пожертвования"""

    comment: Optional[str] = None
    full_amount: PositiveInt


class DonationCreate(DonationBase):
    """Модель для создания пожертвования"""

    pass


class DonationDB(DonationBase):
    """Модель пожертвования для работы с БД"""

    id: int
    user_id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True


class DonationUserDB(BaseModel):
    """Модель пожертвования для отображения пользователю"""

    id: int
    comment: Optional[str] = None
    full_amount: int
    create_date: datetime

    class Config:
        orm_mode = True
