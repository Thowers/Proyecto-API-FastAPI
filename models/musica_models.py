from pydantic import BaseModel
from typing import Dict

class Cancion(BaseModel):
    titulo: str
    artista: str
    genero: str
    popularidad: Dict[str, int]
    fecha_lanzamiento: str