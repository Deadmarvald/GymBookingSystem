from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str
    is_active: bool = True  # Якщо is_active не передається, встановлюється в True


# Схема для створення користувача (вхідні дані)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# Схема для логіну користувача
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Схема для відображення користувача (вихідні дані)
class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# Схема для оновлення користувача (опціональні поля)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


# Схема для відповіді, яка не включатиме пароль
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
