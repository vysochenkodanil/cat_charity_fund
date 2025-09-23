from pydantic import BaseSettings

class Settings(BaseSettings):
    app_title: str = "Cat Charity Fund"
    database_url: str = "sqlite+aiosqlite:///./charity.db"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"

settings = Settings()
