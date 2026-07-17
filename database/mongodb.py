from pymongo import MongoClient

from config import MONGODB_URI, MONGODB_DATABASE


class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DATABASE]


mongodb = MongoDB()
db = mongodb.db