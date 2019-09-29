from utils import *
from bson.objectid import ObjectId
from Place import Place

COLLECTION_NAME = "place"

class PlaceAPI():
    def insert(self, place):
        db = get_db_collection(COLLECTION_NAME)
        users = db.users
        place_id = users.insert_one(place.toQuery()).inserted_id
        return place_id

    def update(self, place):
        if (place.place_id is None):
            print("place_id cannot be None.")
            return
        db = get_db_collection(COLLECTION_NAME)
        users = db.users
        result = users.update_one({ "_id": ObjectId(place.place_id)}, {'$set' : place.toQuery()})
        return result

    def get(self, place_id):
        db = get_db_collection(COLLECTION_NAME)
        users = db.users
        result = users.find_one({ "_id": ObjectId(place_id)})
        place = Place(result["placeName"], result["description"], result["location"], result["rating"], result["_id"])
        return place

    def delete(self, place_id):
        db = get_db_collection(COLLECTION_NAME)
        users = db.users
        result = users.delete_one({ "_id": ObjectId(place_id)})
        return result