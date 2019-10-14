# from utils import get_db_collection
from lib import User
import pymongo
from bson.objectid import ObjectId

COLLECTION_NAME = "Users"

class UserAPI():

    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[COLLECTION_NAME]


    #[input]  user object
    #[return] _id of inserted user
    def insert(self, user):
        srchRlt = self.collection.find_one(user.toQuery())
        if srchRlt is None:
            user_id = self.collection.insert_one(user.toQuery()).inserted_id
        else:
            user_id = srchRlt['_id']
        return user_id


    #[input]  user id
    #[return] user object
    def get(self, userId):
        srchRlt = self.collection.find_one({"userId": userId})
        if srchRlt == None:
            print("The user does not exist")
            return None
        else:
            user = User(srchRlt["userId"], srchRlt["userName"])
            return user

    #[input]  None
    #[return] list of user object
    def list(self):
        results = self.collection.find({})
        users = []
        for result in results:
            user = User(result["userId"], result["userName"])
            users.append(user)
        return users

