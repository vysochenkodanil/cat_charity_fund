from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = "DATABASE_URL"
    secret: str = "SECRET"

    class Config:
        env_file = ".env"

settings = Settings()
