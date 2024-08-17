from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from models import User, Pot, Plant, SensorData

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
    Base.metadata.create_all(bind=engine)
