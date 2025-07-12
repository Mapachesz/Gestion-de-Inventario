from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class Sub_compra(BaseModel):
    id: int = Field(..., ge=0)
    producto_codigo: str = Field(..., min_length=1)
    movimiento_id: int = Field(..., ge=0)
    cantidad: int = Field(..., ge=0)
    subtotal: float = Field(..., gt=0)