from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Usuario(BaseModel):
    email: str
    nombre: str
    numero_control: str
    carrera: str
    estado_beca: str
    rol: str

class Beca(BaseModel):
    numero_control: str
    nombre: str
    carrera: str
    estado: str = "recibida"
    fecha: Optional[datetime] = None