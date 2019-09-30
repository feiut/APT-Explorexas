from PlaceAPI import PlaceAPI
from Place import Place

def testPlaceAPI():
    controller = PlaceAPI()
    print("Test insertion")
    place = Place("dummy name", "dummy description", "dummy location", 5.0)
    inserted_id = controller.insert(place)
    assert(inserted_id is not None)
    print("Passed")

    print("Test list")
    place2 = Place("another dummy name", "another dummy description", "dummy location", 3.0)
    inserted_id2 = controller.insert(place2)
    places = controller.list()
    print("list returns ", len(places), " rows.")
    assert(len(places) >= 2)
    print("Passed")

    print("Test retrieval")
    retrieved = controller.get(inserted_id)
    assert(retrieved.placeName == place.placeName)
    print("Passed")

    print("Test update")
    retrieved.rating = 2.5
    controller.update(retrieved)
    updated = controller.get(inserted_id)
    assert(updated.rating == 2.5)
    print("Passed")

    print("Test deletion")
    result = controller.delete(inserted_id)
    assert(result.deleted_count == 1)
    controller.delete(inserted_id2)
    print("Passed")

# if __name__ == '__main__':
#     testPlaceAPI()