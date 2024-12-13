from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import booking as schemas

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


# Отримати всі бронювання
@router.get("/", response_model=list[schemas.Booking])
def get_all_bookings(db: Session = Depends(database.get_db)):
    bookings = db.query(models.Booking).all()
    return bookings


# Створити нове бронювання
@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(database.get_db)):
    # Перевірка наявності користувача
    user = db.query(models.User).filter(booking.user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Перевірка наявності тренера
    trainer = db.query(models.Trainer).filter(booking.trainer_id == models.Trainer.id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    # Створення бронювання
    new_booking = models.Booking(
        user_id=booking.user_id,
        trainer_id=booking.trainer_id,
        date=booking.date
    )
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking


# Видалити бронювання
@router.delete("/{booking_id}", response_model=schemas.Booking)
def delete_booking(booking_id: int, db: Session = Depends(database.get_db)):
    booking = db.query(models.Booking).filter(booking_id == models.Booking.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    db.delete(booking)
    db.commit()
    return booking
