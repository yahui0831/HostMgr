import os

from pymongo import MongoClient

client = MongoClient(os.environ["MONGODB_ADDR"])
db = client.hostmgr


class BaseModel:

    REQUIRED_FIELDS = []
    COLLECTION = None
    KEY = None

    def __init__(self, data: dict):
        self._data = data

    def __getattr__(self, key: str):
        return self._data[key]

    def update_attr(self, key: str, value: str):
        self._data[key] = value
        self.update()
        return self

    @classmethod
    def create(cls, data: dict):
        # check each field
        for i in cls.REQUIRED_FIELDS:
            if i not in data:
                raise Exception("No {} in date".format(i))
        # insert
        r = cls.COLLECTION.insert_one(data)
        if not r.acknowledged:
            raise Exception("Insert failed!")

        # return user instance, cls(data) == User(data)
        return cls(data)

    def delete(self):
        r = self.COLLECTION.delete_one(self._data)
        if not r.acknowledged:
            raise Exception("Delete failed")

    def update(self):
        if "_id" in self._data:
            del self._data["_id"]

        rt = self.COLLECTION.update_one({self.KEY: self._data[self.KEY]}, {"$set": self._data})
        if not rt.acknowledged:
            raise Exception("Update failed!")
        
        return self

    def json(self):
        item = {}
        for i in self.REQUIRED_FIELDS:
            item[i] = self._data[i]
        return item

    @classmethod
    def query(cls, criteria: dict):
        items = []
        for doc in cls.COLLECTION.find(criteria):
            item = dict(doc)
            if "_id" in item:
                del item["_id"]
            items.append(cls(item))
        return items

class User(BaseModel):

    REQUIRED_FIELDS = ["id", "name", "email", "role"]
    COLLECTION = db.users
    KEY = "id"

    def __init__(self, data: dict):
        super(User, self).__init__(data)


class Machine(BaseModel):

    REQUIRED_FIELDS = ["name", "connection", "occupied_by"]
    COLLECTION = db.machines
    KEY = "name"

    def __init__(self, data):
        super(Machine, self).__init__(data)
