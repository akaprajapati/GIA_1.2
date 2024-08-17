from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL')

# Create the SQLAlchemy engine using the database URL from the settings
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Function to create tables if they don't exist
def create_tables():
    from .models import User, Pot, Plant, SensorData  # Import all your models here
    Base.metadata.create_all(bind=engine)
