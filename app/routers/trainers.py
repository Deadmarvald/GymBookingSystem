from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import trainer as schemas

router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"]
)


# Отримати список всіх тренерів
@router.get("/", response_model=list[schemas.Trainer])
def get_all_trainers(db: Session = Depends(database.get_db)):
    trainers = db.query(models.Trainer).all()
    return trainers


# Створити нового тренера
@router.post("/", response_model=schemas.Trainer)
def create_trainer(trainer: schemas.TrainerCreate, db: Session = Depends(database.get_db)):
    new_trainer = models.Trainer(
        name=trainer.name,
        specialization=trainer.specialization,
        is_available=trainer.is_available
    )
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    return new_trainer


# Оновити інформацію про тренера
@router.put("/{trainer_id}", response_model=schemas.Trainer)
def update_trainer(trainer_id: int, trainer: schemas.TrainerCreate, db: Session = Depends(database.get_db)):
    existing_trainer = db.query(models.Trainer).filter(trainer_id == models.Trainer.id).first()
    if not existing_trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    existing_trainer.name = trainer.name
    existing_trainer.specialization = trainer.specialization
    existing_trainer.is_available = trainer.is_available
    db.commit()
    db.refresh(existing_trainer)
    return existing_trainer


# Видалити тренера
@router.delete("/{trainer_id}", response_model=schemas.Trainer)
def delete_trainer(trainer_id: int, db: Session = Depends(database.get_db)):
    trainer = db.query(models.Trainer).filter(trainer_id == models.Trainer.id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    db.delete(trainer)
    db.commit()
    return trainer
