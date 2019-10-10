from lib import Category
# from utils import get_db_collection
from bson.objectid import ObjectId
import pymongo

COLLECTION_NAME = "Categories"

class CategoryAPI():

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[COLLECTION_NAME]


    #[input]  cat object
    #[return] _id of inserted category
    def insert(self, cat):
        srchRlt = self.collection.find_one(cat.toQuery())
        if srchRlt is None:
            cat_id = self.collection.insert_one(cat.toQuery()).inserted_id
        else:
            cat_id = srchRlt['_id']
        return cat_id

    #[input]  cat object
    #[return] updated result
    def update(self, cat):
        if cat.cat_id is None:
            print("Cat. ID cannot be None")
            return None
        elif self.collection.find_one({"_id": ObjectId(cat.cat_id)}) is None:
            print("Cat. ID does not exist, please create new cat. instead")
            return None
        else:
            return self.collection.update_one({ "_id": ObjectId(cat.cat_id)}, {'$set':cat.toQuery()})

    #[input]  cat id
    #[return] cat object
    def get(self, cat_id):
        srchRlt = self.collection.find_one({"_id": ObjectId(cat_id)})
        if srchRlt == None:
            print("The Category corresponding the input cat. id does not exist")
            return None
        else:
            cat = Category(srchRlt["catName"], srchRlt["catDescription"], srchRlt["pic"], srchRlt["_id"])
            return cat

    #[input]  None
    #[return] list of cat object
    def list(self):
        results = self.collection.find({})
        cats = []
        for result in results:
            cat = Category(result["catName"], result["catDescription"],result["pic"], result["_id"])
            cats.append(cat)
        return cats

    #[input]  cat id
    #[return] deleted result
    def delete(self, cat_id):
        srchRlt = self.collection.find_one({"_id": ObjectId(cat_id)})
        if srchRlt is None:
            print("The Category corresponding the input cat. id does not exist")
            return None
        else:
            result = self.collection.delete_one({"_id": ObjectId(cat_id)})
            return result