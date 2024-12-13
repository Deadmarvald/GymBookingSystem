from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime


# Модель для користувачів
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Відносини
    bookings = relationship("Booking", back_populates="user")


# Модель для тренерів
class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialization = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)

    # Відносини
    bookings = relationship("Booking", back_populates="trainer")


# Модель для бронювань
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Відносини
    user = relationship("User", back_populates="bookings")
    trainer = relationship("Trainer", back_populates="bookings")
