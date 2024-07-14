from datetime import datetime
from pymongo import MongoClient
from store.models.base import CreateBaseModel
from store.schemas.product import ProductIn

# Configuração do cliente MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['store_database']
collection = db['products']

class ProductModel(ProductIn, CreateBaseModel):
    id: int = None
    created_at: datetime = None
    updated_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        product_data = self.dict()
        result = collection.insert_one(product_data)
        self.id = result.inserted_id
        print(f'Produto salvo com ID: {self.id}')

    def update(self, **kwargs):
        updated_fields = {f'set__{k}': v for k, v in kwargs.items()}
        updated_fields['updated_at'] = datetime.now()
        collection.update_one({'_id': self.id}, {'$set': updated_fields})
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.updated_at = updated_fields['updated_at']
        print(f'Produto com ID {self.id} atualizado')

    def delete(self):
        result = collection.delete_one({'_id': self.id})
        if result.deleted_count:
            print(f'Produto com ID {self.id} deletado')
        else:
            print(f'Produto com ID {self.id} não encontrado')

    def __repr__(self):
        return f"<ProductModel id={self.id}, name={self.name}>"
