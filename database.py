from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base


DATABASE_URL = "postgresql://smartpot_user:gia@localhost:5432/smartpot_db"

if not DATABASE_URL:
    raise ValueError("No DATABASE_URL environment variable found.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
