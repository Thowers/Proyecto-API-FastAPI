from fastapi import APIRouter, HTTPException, status, Query
from services.canciones_service import buscar_cancion
from db.database_musica import canciones_collection

router = APIRouter()

@router.get("/canciones")
def obtener_todas_canciones():
    canciones = list(canciones_collection.find({}, {"_id": 0}))
    return {"total": len(canciones), "canciones": canciones}

@router.get("/canciones/buscar/{nombre}", status_code=status.HTTP_200_OK)
def buscar_cancion_endpoint(nombre: str, limite: int = Query(10, description="Cantidad de canciones a devolver")):
    canciones = buscar_cancion(nombre, limite)
    if not canciones:
        raise HTTPException(status_code=404, detail="No se encontraron canciones")
    return canciones