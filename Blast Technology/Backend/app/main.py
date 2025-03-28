# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import SessionLocal, engine
from app.db.base import Base
from app.models.persona import Persona as PersonaModel
from app.schemas.persona import (
    PersonaCreate,
    Persona,
    PersonaUpdate
)

# Crea las tablas en la base de datos (si no existen)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ABM con FastAPI y SQL Server")



# Dependencia para obtener la sesión de DB en cada request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
#      RUTAS DE PERSONA
# --------------------------

@app.post("/crearpersona", response_model=Persona)
def create_persona(persona_in: PersonaCreate, db: Session = Depends(get_db)):
    """Crear una nueva persona."""
    # Verificar si ya existe un email o DNI
    email_existente = db.query(PersonaModel).filter(PersonaModel.email == persona_in.email).first()
    if email_existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado.")

    db_persona = PersonaModel(**persona_in.dict())
    db.add(db_persona)
    db.commit()
    db.refresh(db_persona)
    return db_persona


@app.get("/listarpersona", response_model=List[Persona])
def read_personas(db: Session = Depends(get_db)):
    """Obtener la lista de todas las personas."""
    personas = db.query(PersonaModel).all()
    return personas


@app.get("/idpersona/{persona_id}", response_model=Persona)
def read_persona(persona_id: int, db: Session = Depends(get_db)):
    """Obtener una persona por ID."""
    db_persona = db.query(PersonaModel).filter(PersonaModel.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")
    return db_persona


@app.put("/actualizarpersona/{persona_id}", response_model=Persona)
def update_persona(persona_id: int, persona_in: PersonaUpdate, db: Session = Depends(get_db)):
    """Actualizar una persona por ID."""
    db_persona = db.query(PersonaModel).filter(PersonaModel.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")

    # Actualiza solo los campos que vienen en la petición (exclude_unset=True)
    for field, value in persona_in.dict(exclude_unset=True).items():
        setattr(db_persona, field, value)

    db.commit()
    db.refresh(db_persona)
    return db_persona


@app.delete("/deletepersona/{persona_id}")
def delete_persona(persona_id: int, db: Session = Depends(get_db)):
    """Eliminar una persona por ID."""
    db_persona = db.query(PersonaModel).filter(PersonaModel.id == persona_id).first()
    if not db_persona:
        raise HTTPException(status_code=404, detail="Persona no encontrada.")

    db.delete(db_persona)
    db.commit()
    return {"detail": "Persona eliminada con éxito"}


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)