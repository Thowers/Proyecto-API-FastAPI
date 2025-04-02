from fastapi import APIRouter, HTTPException
from db import database_musica as db
from models.musica_models import Cancion
from services.musica_services import agregar_cancion, obtener_canciones_populares

router = APIRouter()

@router.post("/canciones/")
async def agregar_cancion_endpoint():
    try:
        cancion = agregar_cancion(cancion)
        return {"mensaje": "Canción agregada", "id": str(cancion.inserted_id)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar canción: {str(e)}")

@router.get("/canciones/populares")
async def obtener_canciones_populares_endpoint():
    try:
        canciones = obtener_canciones_populares()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener canciones populares: {str(e)}")
    return canciones
