from pymongo import MongoClient
import settings


class Database:
    def __init__(self):
        client = MongoClient(
            f"mongodb+srv://{settings.MONGO_DB_USERNAME}:{settings.MONGO_DB_PASSWORD}@database.wgwik.mongodb.net")
        self.__data = client[settings.MONGO_DB_NAME]

    def get(self, table: str, where: dict) -> dict:
        item = self.__data[table].find_one(where, sort=[("token", 1)])
        if item is not None:
            del item["_id"]
        return item

    def set(self, table: str, data: dict) -> int:
        item = self.__data[table].find_one(sort=[("id", -1)])
        data["id"] = item["id"]+1 if item else 1
        self.__data[table].insert_one(data)
        return data["id"]
