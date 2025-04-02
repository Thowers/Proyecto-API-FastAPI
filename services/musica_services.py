from db.database_musica import database
from bson import ObjectId
from models.musica_models import Cancion

def agregar_cancion(cancion: Cancion):
    resultado = database.canciones.insert_one(cancion.dict())
    return {"mensaje": "Canción agregada", "id": str(resultado.inserted_id)}

def obtener_canciones_populares():
    canciones = list(database.canciones.find().sort("popularidad", -1).limit(10))
    for cancion in canciones:
        cancion["_id"] = str(cancion["_id"])
    return canciones