from core.db import MongoDBDataManager


class OCRLLM_Quote_CRUD(MongoDBDataManager):

    def __init__(self):
        super().__init__()
        self.db_name = 'ocrllm'
        self.collection_name = 'quotes'

    def get_db_collection(self):
        return self.db_client[self.db_name][self.collection_name]

    def save_quote(self, document):
        mdb_collection = self.get_db_collection()
        result = mdb_collection.insert_one(document)
        return result.inserted_id