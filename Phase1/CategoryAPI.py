from utils import *
from bson.objectid import ObjectId
from Category import Category

COLLECTION_NAME = "Categories"

class CategoryAPI():
    #[input]  cat object
    #[return] _id of inserted category
    def insert(self, cat):
        collection = get_db_collection(COLLECTION_NAME)
        srchRlt = collection.find_one(cat.toQuery())
        if srchRlt is None:
            cat_id = collection.insert_one(cat.toQuery()).inserted_id
        else:
            cat_id = srchRlt['_id']
        return cat_id

    #[input]  cat object
    #[return] updated result
    def update(self, cat):
        collection = get_db_collection(COLLECTION_NAME)
        if cat.cat_id is None:
            print("Cat. ID cannot be None")
            return None
        elif collection.find_one({"_id": ObjectId(cat.cat_id)}) is None:
            print("Cat. ID does not exist, please create new cat. instead")
            return None
        else:
            return collection.update_one({ "_id": ObjectId(cat.cat_id)}, {'$set':cat.toQuery()})

    #[input]  cat id
    #[return] cat object
    def get(self, cat_id):
        collection = get_db_collection(COLLECTION_NAME)
        srchRlt = collection.find_one({"_id": ObjectId(cat_id)})
        if srchRlt == None:
            print("The Category corresponding the input cat. id does not exist")
            return None
        else:
            cat = Category(srchRlt["catName"], srchRlt["_id"])
            return cat

    #[input]  None
    #[return] list of cat object
    def list(self):
        collection = get_db_collection(COLLECTION_NAME)
        results = collection.find({})
        cats = []
        for result in results:
            cat = Category(result["catName"], result["_id"])
            cats.append(cat)
        return cats

    #[input]  cat id
    #[return] deleted result
    def delete(self, cat_id):
        collection = get_db_collection(COLLECTION_NAME)
        srchRlt = collection.find_one({"_id": ObjectId(cat_id)})
        if srchRlt is None:
            print("The Category corresponding the input cat. id does not exist")
            return None
        else:
            result = collection.delete_one({"_id": ObjectId(cat_id)})
            return result
