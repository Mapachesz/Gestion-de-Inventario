from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from typing import Optional

class Movimientos(BaseModel):
    id: int = Field(..., ge=0)
    tipo: str
    fecha: Optional[date] = None
    total: float = Field(..., gt=0)
    cliente_rut: Optional[str] = Field(default=None, min_length=8)