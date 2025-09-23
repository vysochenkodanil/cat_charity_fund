from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional, Union

class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: int = Field(..., gt=0)

class CharityProjectCreate(CharityProjectBase):
    pass

class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)

class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = 0
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
