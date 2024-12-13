from pydantic import BaseModel
from typing import Optional


# Схема для створення тренера (вхідні дані)
class TrainerCreate(BaseModel):
    name: str
    specialization: Optional[str] = None
    is_available: Optional[bool] = True


# Схема для відображення тренера (вихідні дані)
class Trainer(BaseModel):
    id: int
    name: str
    specialization: Optional[str] = None
    is_available: bool

    class Config:
        from_attributes = True
