# app/models/persona.py
from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Persona(Base):
    __tablename__ = "Usuario"  # Nombre de la tabla en tu base de datos

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    dni = Column(String(20), nullable=True, unique=True)
    nro_telefono = Column(String(20), nullable=True)
    direccion = Column(String(100), nullable=True)
