
from utils import get_db_collection
from User import User
from bson.objectid import ObjectId

COLLECTION_NAME = "Users"

class UserCollectionAPI():

    def insert(self, user):
        collection = get_db_collection(COLLECTION_NAME)
        query = {'username': user.username}
        searchResult = collection.find_one(query)
        if searchResult is None:
            user_id = collection.insert_one(user.toQuery()).inserted_id
            return user_id
        else:
            # If existed, then prompt error
            print('The user already exists, id is:' + str(searchResult['_id']))
            return searchResult['_id']


    def delete(self, field, value):
        collection = get_db_collection(COLLECTION_NAME)
        if(field == '_id'):
            query = {'_id': ObjectId(value)}
        else:
            query = {field: value}
        if (collection.find_one(query) is not None):
            # If the username exists, then delete it
            result = collection.delete_one(query)
            return result
        else:
            print('User not existed.')


    def update(self, user):
        collection = get_db_collection(COLLECTION_NAME)
        query = {'_id': user.user_id}
        # Update a user's info according to username
        if (collection.find_one(query) is not None):
            # If the user exists, update
            result = collection.update_one({"_id":ObjectId(user.user_id)}, {"$set": user.toQuery()})
            return result
        else:
            print('User ' + user.user_id + ' not existed.')


    def get(self, field, value):
        collection = get_db_collection(COLLECTION_NAME)
        if(field == '_id'):
            result = collection.find_one({'_id': ObjectId(value)})
        else:
            result = collection.find_one({field: value})
        user = User(result["username"], result["password"], result["email"], result["gender"], result["dateOfBirth"],
                    result["dateOfRegistration"], result["role"], result["_id"])
        return user


    def list(self):
        collection = get_db_collection(COLLECTION_NAME)
        results = collection.find({})
        users = []
        for result in results:
            user = User(result["username"], result["password"], result["email"], result["gender"], result["dateOfBirth"],
                        result["dateOfRegistration"], result["role"], result["_id"])
            users.append(user)
        return users
