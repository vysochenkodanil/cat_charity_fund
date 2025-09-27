from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Cat Charity Fund"
    database_url: str = "sqlite+aiosqlite:///./charity.db"
    secret: str = "SECRET"
    password_len: int = 3
    minute: int = 3600

    class Config:
        env_file = ".env"


settings = Settings()
