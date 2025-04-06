from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(os.getenv("MONGO_URI"), tlsallowinvalidcertificates=True)
        self.db = self.client[os.getenv("MONGO_COLLECTION")]

    def get_collection(self, collection):
        return self.db[collection]
        
database = Database()