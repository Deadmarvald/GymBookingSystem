from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.db.database import SessionLocal
from app.schemas import user
from app.db import models
from app.utils.security import verify_password, get_password_hash, create_access_token
from sqlalchemy.orm import Session
from app.routers import users, trainers, bookings  # Імпортуємо всі роутери з директорії

# Ініціалізація додатка
app = FastAPI(
    title="Gym Booking System",
    description="API для бронювання спортивних тренувань",
    version="1.0.0"
)

# Підключення шаблонів
templates = Jinja2Templates(directory="app/templates")


# Функція для отримання сесії бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Підключення роутерів з директорії "routers"
app.include_router(users.router)  # Роутери для користувачів
app.include_router(trainers.router)  # Роутери для тренерів
app.include_router(bookings.router)  # Роутери для бронювань


# Реєстрація користувача
@app.post("/register", response_model=user.UserCreate)
def register_user(user: user.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(user.email == models.User.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# Логін користувача
@app.post("/login")
def login_user(user: user.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(user.email == models.User.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Головна сторінка
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Сторінка реєстрації
@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


# Сторінка логіну
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
