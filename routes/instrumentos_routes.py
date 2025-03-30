from fastapi import APIRouter, HTTPException, status
from models.instrumento_models import Instrumento
from services.instrumento_services import obtener_instrumentos, obtener_instrumento_por_id, insertar_instrumento, actualizar_instrumento, eliminar_instrumento

router = APIRouter()

@router.get('/instrumentos', response_model=list, status_code=status.HTTP_200_OK)
async def obtener_instrumentos_endpoint():
    instrumentos = obtener_instrumentos()
    if not instrumentos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hay Stock de instrumentos")
    return instrumentos

@router.get('/instrumentos/{instrumento_id}', response_model=Instrumento, status_code=status.HTTP_200_OK)
def obtener_instrumento_por_id_endpoint(instrumento_id: str):
    instrumento = obtener_instrumento_por_id(instrumento_id)
    if not instrumento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
    return instrumento

@router.post('/instrumentos')
async def insertar_instrumento_endpoint(instrumento: Instrumento, status_code=status.HTTP_201_CREATED):
    try:
        instrumento_id = insertar_instrumento(instrumento)
        return {"mensaje": "Instrumento insertado correctamente", "instrumento_id": instrumento_id}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al insertar el instrumento: {str(e)}")

@router.put('/instrumentos/{instrumento_id}')
async def actualizar_instrumento_endpoint(instrumento_id: str, instrumento: Instrumento, status_code=status.HTTP_200_OK):
    try:
        resultado = actualizar_instrumento(instrumento_id, instrumento)
        if resultado.get("mensaje") == "Instrumento no encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al actualizar el instrumento: {str(e)}")
    
@router.delete('/instrumentos/{instrumento_id}')
async def eliminar_instrumento_endpoint(instrumento_id: str, status_code=status.HTTP_200_OK):
    try:
        resultado = eliminar_instrumento(instrumento_id)
        if resultado.get("mensaje") == "Instrumento no encontrado":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instrumento no encontrado")
        return resultado
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error al eliminar el instrumento: {str(e)}")    