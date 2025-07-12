from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Producto(BaseModel):
    codigo: str = Field(..., min_length=1)
    nombre: str
    descripcion: Optional[str] = None
    stock: int = Field(..., ge=0)
    precio_unitario: float = Field(..., gt=0)
    fecha_ingreso: Optional[date] = None

