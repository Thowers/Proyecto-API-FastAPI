from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb+srv://towers1904:nikolash190499@clusterthowers.ixmyw.mongodb.net/?retryWrites=true&w=majority&appName=ClusterThowers', tlsallowinvalidcertificates=True)
        self.db = self.client['MusiCenter']

    def get_collection(self, collection):
        return self.db[collection]
        
database = Database()