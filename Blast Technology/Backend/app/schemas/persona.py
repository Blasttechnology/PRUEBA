# app/schemas/persona.py
from pydantic import BaseModel, EmailStr
from typing import Optional

class PersonaBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    dni: Optional[str] = None
    nro_telefono: Optional[str] = None
    direccion: Optional[str] = None

class PersonaCreate(PersonaBase):
    """
    Schema para crear una nueva persona.
    Puede ser igual a PersonaBase, 
    pero si tuvieras campos obligatorios extra, los pones aquí.
    """
    pass

class PersonaUpdate(PersonaBase):
    """
    Schema para actualizar una persona.
    Permite campos opcionales, 
    si quieres manejar actualizaciones parciales.
    """
    pass

class PersonaInDBBase(PersonaBase):
    id: int

    class Config:
        orm_mode = True

# Schema de respuesta
class Persona(PersonaInDBBase):
    pass
