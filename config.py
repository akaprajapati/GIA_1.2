from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str

    class Config:
        env_file = ".env"  # This tells pydantic to load variables from a .env file

# Load the settings
settings = Settings()
