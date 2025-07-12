from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Clientes(BaseModel):
    rut: str = Field(..., min_length=8)
    nombre: str
    direccion: str
    celular: str = Field(..., min_length=8)
    correo: str