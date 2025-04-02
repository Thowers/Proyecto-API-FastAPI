from pydantic import BaseModel
from typing import List, Optional

class Instrumento(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = None

