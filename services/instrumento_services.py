from db.database import database
from bson import ObjectId
from models.instrumento_models import Instrumento

def obtener_instrumentos():
    collection = database.get_collection('instrumentos')
    instrumentos = list(collection.find({}, {'_id': 0}))
    return instrumentos

#instrumento por id
def obtener_instrumento_por_id(instrumento_id: str):
    collection = database.get_collection('instrumentos')
    try:
        inst_id = ObjectId(instrumento_id)
    except:
        return None
    
    instrumento = collection.find_one({'_id': inst_id})

    if instrumento:
        return Instrumento(**instrumento)
    return None

#insertar instrumento
def insertar_instrumento(instrumento: Instrumento):
    collection = database.get_collection('instrumentos')
    instrumento_dict = instrumento.dict()
    result = collection.insert_one(instrumento_dict)
    return {'_id': str(result.inserted_id), 'mensaje': 'Instrumento insertado correctamente'}

#actualizar instrumento
def actualizar_instrumento(instrumento_id: str, instrumento: Instrumento):
    collection = database.get_collection('instrumentos')
    updated_instrumento = {}
    instrument_dict = instrumento.dict()
    for key, value in instrument_dict.items():
        if value is not None:
            updated_instrumento[key] = value
    if not updated_instrumento:
        return {"mensaje":"Mijo, no se actualizo nada"}
    resultado = collection.update_one({"_id": ObjectId(instrumento_id)},{"$set": updated_instrumento})
    print(resultado)
    if resultado.modified_count == 0:
        return {"mensaje":"Instrumento no encontrado"}
    return {"mensaje":"Instrumento actualizado correctamente"}

#eliminar instrumento
def eliminar_instrumento(instrumento_id: str):
    collection = database.get_collection('instrumentos')
    try:
        inst_id = ObjectId(instrumento_id)
    except:
        return None    
    resultado = collection.delete_one({"_id": inst_id})
    if resultado.deleted_count == 0:
        return {"mensaje":"Instrumento no encontrado"}
    return {"mensaje":"Instrumento eliminado correctamente"}