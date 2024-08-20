from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from auth import get_current_user_id,hash_password,verify_password,create_access_token
from fastapi.security import OAuth2PasswordRequestForm
import models
from database import SessionLocal, engine, Base, create_tables, create_engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Ensure that the tables are created at startup
@app.on_event("startup")
def startup_event():
    create_tables()  # Create tables if they don't exist

# Pydantic models for request validation
class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class PotCreate(BaseModel):
    name: str

class PlantCreate(BaseModel):
    species: str
    nickname: str = None

class SensorDataCreate(BaseModel):
    moisture: float
    light: float
    temperature: float


# User registration
@app.post("/register/")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Hash the password and create the user
    password_hash = hash_password(user.password)
    db_user = models.User(username=user.username, email=user.email, password_hash=password_hash)  # Update to use password_hash
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Smart Pot API!"}


# Login endpoint to authenticate the user and return a token
@app.post("/token/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):  # Update to use password_hash
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# Create a pot
@app.post("/pots", response_model=dict)
def create_pot(pot: PotCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    db_pot = models.Pot(name=pot.name, user_id=user_id)
    db.add(db_pot)
    db.commit()
    db.refresh(db_pot)
    return {"id": db_pot.id}

# Add a plant to a pot
@app.post("/pots/{pot_id}/plants", response_model=dict)
def add_plant(pot_id: str, plant: PlantCreate, db: Session = Depends(get_db)):
    db_plant = models.Plant(pot_id=pot_id, species=plant.species, nickname=plant.nickname)
    db.add(db_plant)
    db.commit()
    db.refresh(db_plant)
    return {"id": db_plant.id}

# Add sensor data
@app.post("/plants/{plant_id}/sensordata", response_model=dict)
def add_sensor_data(plant_id: str, sensor_data: SensorDataCreate, db: Session = Depends(get_db)):
    db_sensor_data = models.SensorData(plant_id=plant_id, moisture=sensor_data.moisture, 
                                       light=sensor_data.light, temperature=sensor_data.temperature)
    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    return {"id": db_sensor_data.id}


#codes to get the data online 
# GET route to fetch all pots
@app.get("/pots/")
def get_all_pots(db: Session = Depends(get_db)):
    pots = db.query(models.Pot).all()
    return pots


# GET route to fetch a specific pot by name
@app.get("/pots/{pot_name}")
def get_pot_by_name(pot_name: str, db: Session = Depends(get_db)):
    pot = db.query(models.Pot).filter(models.Pot.name == pot_name).first()
    if not pot:
        raise HTTPException(status_code=404, detail=f"Pot with name '{pot_name}' not found.")
    return pot

# GET route to fetch all plants in a specific pot by pot name
@app.get("/pots/{pot_name}/plants/")
def get_plants_by_pot_name(pot_name: str, db: Session = Depends(get_db)):
    pot = db.query(models.Pot).filter(models.Pot.name == pot_name).first()
    if not pot:
        raise HTTPException(status_code=404, detail=f"Pot with name '{pot_name}' not found.")
    
    plants = db.query(models.Plant).filter(models.Plant.pot_id == pot.id).all()
    return plants

# GET route to fetch a specific plant by plant ID
@app.get("/plants/{plant_id}")
def get_plant_by_id(plant_id: str, db: Session = Depends(get_db)):
    plant = db.query(models.Plant).filter(models.Plant.id == plant_id).first()
    if not plant:
        raise HTTPException(status_code=404, detail=f"Plant with ID '{plant_id}' not found.")
    return plant


@app.get("/sensordata", response_model=list)
def get_sensor_data(
    plant_id: str = Query(None, description="Filter by plant ID"),
    db: Session = Depends(get_db),
    user_id: str = Depends(get_current_user_id)
):
    if plant_id:
        # Get sensor data for a specific plant
        sensor_data = db.query(SensorData).filter(SensorData.plant_id == plant_id).all()
        if not sensor_data:
            raise HTTPException(status_code=404, detail="No sensor data found for the given plant ID")
    else:
        # Get all sensor data
        sensor_data = db.query(SensorData).all()

    return sensor_data


