from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"  # Вказуємо шлях до файлу .env


# Ініціалізація об'єкта налаштувань
settings = Settings()
