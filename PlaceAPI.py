from utils import *
from bson.objectid import ObjectId
from Place import Place

COLLECTION_NAME = "place"

class PlaceAPI():
    def insert(self, place):
        collection = get_db_collection(COLLECTION_NAME)
        place_id = collection.insert_one(place.toQuery()).inserted_id
        return place_id

    def update(self, place):
        if (place.place_id is None):
            print("place_id cannot be None.")
            return
        collection = get_db_collection(COLLECTION_NAME)
        result = collection.update_one({ "_id": ObjectId(place.place_id)}, {'$set' : place.toQuery()})
        return result

    def get(self, place_id):
        collection = get_db_collection(COLLECTION_NAME)
        result = collection.find_one({ "_id": ObjectId(place_id)})
        place = Place(result["placeName"], result["description"], result["location"], result["rating"], result["_id"])
        return place

    def list(self):
        collection = get_db_collection(COLLECTION_NAME)
        results = collection.find({ })
        places = []
        for result in results:
            place = Place(result["placeName"], result["description"], result["location"], result["rating"], result["_id"])
            places.append(place)
        return places

    def delete(self, place_id):
        collection = get_db_collection(COLLECTION_NAME)
        result = collection.delete_one({ "_id": ObjectId(place_id)})
        return result