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

from tortoise.contrib.fastapi import register_tortoise

DB_ROOT = "db"  # root directory for database files
DB_NAME = "hsms_vip.db"  # database filename
SQLITE_URL = f"sqlite://./{DB_ROOT}/{DB_NAME}"

def init_db_sqlite(app):
    """
    Initialize the database with sqlite
    :param app: FastAPI app instance
    :return:
    """
    register_tortoise(
        app,
        db_url=SQLITE_URL,
        modules={"models": ["models"]},
        generate_schemas=True,  # We need to generate schemas
        add_exception_handlers=True,
    )

