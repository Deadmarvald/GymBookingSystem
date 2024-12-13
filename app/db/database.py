from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Завантаження змінних з .env
load_dotenv()

# URL бази даних із файлу .env
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in .env file")

# Створення об'єкта двигуна SQLAlchemy
engine = create_engine(DATABASE_URL)

# Створення фабрики сесій
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для моделей
Base = declarative_base()

# Залежність для отримання сесії
def get_db():
    """
    Отримує сесію для роботи з базою даних.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
