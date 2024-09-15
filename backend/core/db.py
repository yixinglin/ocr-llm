from core.config import config
from core.logs import logger
import pymongo
from pymongo.errors import ServerSelectionTimeoutError


MONGO_CONFIG = config.mongodb


class MongoDBDataManager:

    def __init__(self):
        self.db_host = MONGO_CONFIG.uri
        self.db_port = MONGO_CONFIG.port
        self.db_client = None

    def connect(self):
        # Connect to MongoDB
        try:
            self.db_client = pymongo.MongoClient(self.db_host, self.db_port, serverSelectionTimeoutMS=10000)  # Connect
            names = self.db_client.list_database_names()
        except ServerSelectionTimeoutError as e:
            logger.error(f"Error connecting to MongoDB: {e}")
            raise RuntimeError("Error connecting to MongoDB")
        return self

    def get_client(self):
        return self.db_client

    def set_client(self, client):
        self.db_client = client
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        del self

    def close(self):
        if self.db_client:
            self.db_client.close()