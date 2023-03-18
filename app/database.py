from pymongo import MongoClient
from pymongo.collection import Collection
from .core.settings import mongo_settings as settings

__all__ = ("client", "collection")
client = MongoClient(settings.uri)
# client = MongoClient("mongodb://localhost:27017")

users: Collection = client[settings.database]["users"]
interfaces: Collection = client[settings.database]["interface"]
templete: Collection = client[settings.database]["templete"]
notification: Collection = client[settings.database]["notification"]

