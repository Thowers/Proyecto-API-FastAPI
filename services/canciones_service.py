from spotify_api import sp
from db.database_musica import canciones_collection, artistas_collection, estadisticas_collection
from bson import ObjectId
from pymongo import DESCENDING

def actualizar_estadisticas():
    top = list(canciones_collection.find({}, {"_id": 0}).sort("popularidad", -1).limit(10))
    estadisticas_collection.delete_many({})
    if top:
        estadisticas_collection.insert_many(top)

def buscar_cancion(nombre: str, limite: int = 1):
    canciones_existentes = list(canciones_collection.find({"titulo": {"$regex": f"^{nombre}$", "$options": "i"}},{"_id": 0}))    
    if canciones_existentes:
        return canciones_existentes     
    resultados = sp.search(q=nombre, limit=limite, type="track")  
    if not resultados["tracks"]["items"]:
        return None
    canciones = []
    for cancion in resultados["tracks"]["items"]:
        artist_id = cancion["artists"][0]["id"]
        artist_info = sp.artist(artist_id)
        genres = artist_info.get("genres", [])
        release_date = cancion["album"].get("release_date", "No especificado")
        cancion_data = {
            "titulo": cancion["name"],
            "artista": cancion["artists"][0]["name"],
            "popularidad": cancion["popularity"],
            "album": cancion["album"]["name"],
            "imagen": cancion["album"]["images"][0]["url"],
            "genero": genres[0] if genres else "No especificado",
            "fecha_lanzamiento": release_date
        }        
        resultado_insert = canciones_collection.insert_one(cancion_data)
        cancion_data["_id"] = str(resultado_insert.inserted_id) 
        canciones.append(cancion_data)
        artista_nombre = cancion_data["artista"]
        artista = artistas_collection.find_one({"nombre": artista_nombre})
        if artista:
            if "canciones" in artista:
                if cancion_data["titulo"] not in artista["canciones"]:artistas_collection.update_one({"nombre": artista_nombre},{"$push": {"canciones": cancion_data["titulo"]}})
            else:
                artistas_collection.update_one({"nombre": artista_nombre},{"$set": {"canciones": [cancion_data["titulo"]]}})
        else:
            artistas_collection.insert_one({"nombre": artista_nombre, "canciones": [cancion_data["titulo"]]})    
    actualizar_estadisticas()
    return canciones

def obtener_estadisticas_resumen():
    total_canciones = canciones_collection.count_documents({})
    pipeline_promedio = [{"$group": {"_id": None,"promedio_popularidad": {"$avg": "$popularidad"}}}]
    resultado_promedio = list(canciones_collection.aggregate(pipeline_promedio))
    promedio_popularidad = resultado_promedio[0]["promedio_popularidad"] if resultado_promedio else 0
    cancion_top = canciones_collection.find_one(sort=[("popularidad", DESCENDING)], projection={"_id": 0})
    pipeline_artistas = [{"$group": {"_id": "$artista","total canciones": {"$sum": 1}}},
        {"$sort": {"total canciones": -1}},
        {"$limit": 10}
    ]
    resultado_artistas = list(canciones_collection.aggregate(pipeline_artistas))
    artistas_mas_populares = resultado_artistas[0] if resultado_artistas else {"_id": "N/A", "cantidad": 0}

    return {
        "total canciones": total_canciones,
        "promedio popularidad":round(promedio_popularidad, 2),
        "cancion top": cancion_top,
        "artistas mas populares": {
            "nombre": artistas_mas_populares["_id"]},
            "cantidad de canciones": artistas_mas_populares["total canciones"]
    }