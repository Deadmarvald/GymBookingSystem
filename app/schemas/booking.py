from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Схема для створення бронювання (вхідні дані)
class BookingCreate(BaseModel):
    user_id: int
    trainer_id: int
    date: datetime


# Схема для відображення бронювання (вихідні дані)
class Booking(BaseModel):
    id: int
    user_id: int
    trainer_id: int
    date: datetime

    class Config:
        from_attributes = True
