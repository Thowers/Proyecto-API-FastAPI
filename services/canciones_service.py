from spotify_api import sp
from db.database_musica import canciones_collection
from bson import ObjectId

def buscar_cancion(nombre: str, limite: int = 1):
    canciones_existentes = list(canciones_collection.find({"titulo": nombre}, {"_id": 0}))
    
    if canciones_existentes:
        return canciones_existentes 

    
    resultados = sp.search(q=nombre, limit=limite, type="track")  
    if not resultados["tracks"]["items"]:
        return None

    canciones = []
    for cancion in resultados["tracks"]["items"]:
        cancion_data = {
            "titulo": cancion["name"],
            "artista": cancion["artists"][0]["name"],
            "popularidad": cancion["popularity"],
            "album": cancion["album"]["name"],
            "imagen": cancion["album"]["images"][0]["url"],
            "preview_url": cancion.get("preview_url", "No disponible")
        }
        
        resultado_insert = canciones_collection.insert_one(cancion_data)
        cancion_data["_id"] = str(resultado_insert.inserted_id) 

        canciones.append(cancion_data)

    return canciones