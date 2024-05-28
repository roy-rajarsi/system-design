from .mongodb_connection import MongoDbClientConnection
from .mongodbdocument import MongoDbDocument

from abc import ABC
from datetime import date, datetime
from decimal import Decimal
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict, List, Optional, Union


class MongoDbCollection(ABC):

    __mongodb_client_connection: MongoDbClientConnection = MongoDbClientConnection()

    def __init__(self, collection_name: str) -> None:
        self.__database: [Database] = MongoDbCollection.__mongodb_client_connection.connection['splitwise']
        self.__collection: Collection = self.__database[collection_name]

    def get_first_document(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]) -> MongoDbDocument:
        return MongoDbDocument(data=self.__collection.find_one(filter=filter))

    def get_documents(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']], limit: Optional[int] = None) -> List[MongoDbDocument]:
        if limit is None:
            return [MongoDbDocument(data=document) for document in self.__collection.find(filter=filter)]
        else:
            return [MongoDbDocument(data=document) for document in self.__collection.find(filter=filter).limit(limit)]

    def get_all_documents(self) -> List[MongoDbDocument]:
        return [MongoDbDocument(data=document) for document in self.__collection.find(filter={})]

    def save_document(self, document: MongoDbDocument) -> None:
        self.__collection.insert_one(document=document.get_key_value_pairs())

    def save_documents_in_bulk(self, list_of_documents: List[MongoDbDocument], ordered: bool = False) -> None:
        self.__collection.insert_many(documents=[document.get_key_value_pairs() for document in list_of_documents], ordered=ordered)

    def patch_first_document(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']], updated_document: MongoDbDocument) -> None:
        self.__collection.update_one(filter=filter, update=updated_document.get_key_value_pairs())

    def patch_all_documents(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']], updated_document: MongoDbDocument) -> None:
        self.__collection.update_many(filter=filter, update=updated_document.get_key_value_pairs())

    def delete_first_document(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]) -> None:
        self.__collection.delete_one(filter=filter)

    def delete_all_documents(self, filter: Dict[str, Union[bool, Decimal, int, str, date, datetime, 'MongoDbDocument']]) -> None:
        self.__collection.delete_many(filter=filter)

    def __repr__(self) -> str:
        return f'MongoDbCollection(Database: {self.__database.name} Collection: {self.__collection.name})'
