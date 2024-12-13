from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import models, database
from app.schemas import user as schemas
from app.db.database import get_db
from app.utils.security import get_password_hash, verify_password, create_access_token


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Отримати список усіх користувачів
@router.get("/", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users


# Реєстрація користувача
@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Перевіряємо, чи вже існує користувач з таким email
    existing_user = db.query(models.User).filter(user.email == models.User.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Хешуємо пароль перед збереженням
    hashed_password = get_password_hash(user.password)

    # Створюємо нового користувача
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    # Шукаємо користувача в базі даних
    db_user = db.query(models.User).filter(user.email == models.User.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Створюємо токен для аутентифікації
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Отримати користувача за ID
@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Створити нового користувача
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(user.email == models.User.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=user.password,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# Оновити дані користувача
@router.put("/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(database.get_db)):
    existing_user = db.query(models.User).filter(user_id == models.User.id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.name is not None:
        existing_user.name = user.name
    if user.email is not None:
        existing_user.email = user.email
    if user.password is not None:
        existing_user.password = user.password  # Хешуйте паролі у реальних проєктах!
    if user.is_active is not None:
        existing_user.is_active = user.is_active

    db.commit()
    db.refresh(existing_user)
    return existing_user


# Видалити користувача
@router.delete("/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(user_id == models.User.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user
