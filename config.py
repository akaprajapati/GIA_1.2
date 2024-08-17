import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:gia_smart@localhost:5432/postgres")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "secretkeyexample")
    ALGORITHM: str = "HS256"

settings = Settings()
