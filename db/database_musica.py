from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"), tlsallowinvalidcertificates=True)
        self.db = self.client[os.getenv("MONGO_COLLECTION2")]

    def get_collection(self, collection):
        return self.db[collection]
        
database = Database()
canciones_collection = database.get_collection('canciones')
artistas_collection = database.get_collection('artistas')
estadisticas_collection = database.get_collection('estadisticas')

