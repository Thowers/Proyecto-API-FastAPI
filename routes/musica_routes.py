from fastapi import APIRouter, HTTPException, status, Query
from db.database_musica import canciones_collection, artistas_collection, estadisticas_collection
from models.musica_models import Cancion
from services.musica_services import buscar_cancion, obtener_estadisticas_resumen

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

@router.get("/canciones/top", status_code=status.HTTP_200_OK)
def obtener_canciones_populares():
    canciones = list(canciones_collection.find({}, {"_id": 0}).sort("popularidad", -1).limit(10))
    return {"total": len(canciones), "canciones": canciones}

@router.get("/artistas", status_code=status.HTTP_200_OK)
def obtener_artistas():
    artistas = list(artistas_collection.find({}, {"_id": 0, "nombre": 1}))
    artistas = [{"nombre": artista["nombre"]} for artista in artistas]
    return {"total": len(artistas), "artistas": artistas}

@router.get("/estadisticas/resumen", status_code=status.HTTP_200_OK)
def obtener_estadisticas():
    return obtener_estadisticas_resumen()

# @router.delete("/admin/clear", status_code=status.HTTP_200_OK)
# def clear_collections():
#     try:
#         canciones_collection.delete_many({})
#         artistas_collection.delete_many({})
#         estadisticas_collection.delete_many({})
#         return {"mensaje": "Todas las colecciones han sido limpiadas."}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error al limpiar las colecciones: {str(e)}")
