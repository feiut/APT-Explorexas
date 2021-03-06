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
            subscription = []
            try:
                subscription = srchRlt["subscription"]
            except Exception as exc:
                pass
            user = User.User(srchRlt["userId"], srchRlt["userName"], subscription)
            return user

    #[input]  None
    #[return] list of user object
    def list(self):
        results = self.collection.find({})
        users = []
        for result in results:
            subscription = []
            try:
                subscription = result["subscription"]
            except Exception as exc:
                pass

            user = User.User(result["userId"], result["userName"], subscription)
            users.append(user)
        return users

    #[input]  None
    #[return] list of user object
    def subscribe(self, userId, authorId):
        return self.collection.update_one({ "userId": userId}, {'$push': {'subscription': authorId}})
    
    def unsubscribe(self, userId, authorId):
        return self.collection.update_one({ "userId": userId}, {'$pull': {'subscription': authorId}})

    
    def close_connection(self):
        self.client.close()