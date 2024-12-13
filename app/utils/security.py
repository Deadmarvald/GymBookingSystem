from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings
from typing import Union

# Налаштування для хешування паролів
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хешування пароля
def get_password_hash(password: str) -> str:
    """
    Хешує пароль за допомогою bcrypt.
    """
    return pwd_context.hash(password)


# Перевірка пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Порівнює звичайний текстовий пароль із хешованим паролем.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Генерація JWT токена
def create_access_token(data: dict) -> str:
    """
    Створює JWT токен із заданими даними та терміном дії.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


# Розшифровка та перевірка JWT токена
def decode_access_token(token: str) -> dict | None:
    """
    Розшифровує JWT токен та перевіряє його дійсність.
    """
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return decoded_token if datetime.utcnow() < datetime.utcfromtimestamp(decoded_token["exp"]) else None
    except JWTError:
        return None
