from sqlalchemy import Column, String, Float, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
import uuid
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    pots = relationship('Pot', back_populates='user', cascade="all, delete-orphan")

class Pot(Base):
    __tablename__ = 'pots'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship('User', back_populates='pots')


    # Relationship with the User model
    user = relationship('User', back_populates='pots')

    # Relationship with the Plant model
    plants = relationship('Plant', back_populates='pot', cascade="all, delete-orphan")


class Plant(Base):
    __tablename__ = 'plants'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pot_id = Column(UUID(as_uuid=True), ForeignKey('pots.id'), nullable=False)
    species = Column(String, nullable=False)
    nickname = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    pot = relationship('Pot', back_populates='plants')


    # Relationship with the Pot model
    pot = relationship('Pot', back_populates='plants')

    # Relationship with the SensorData model
    sensordata = relationship('SensorData', back_populates='plant', cascade="all, delete-orphan")


class SensorData(Base):
    __tablename__ = 'sensordata'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    plant_id = Column(UUID(as_uuid=True), ForeignKey('plants.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    moisture = Column(Float, nullable=False)
    light = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    plant = relationship('Plant', back_populates='sensordata')


    # Relationship with the Plant model
    plant = relationship('Plant', back_populates='sensordata')
