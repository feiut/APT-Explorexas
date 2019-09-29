class Place:
    
    def __init__(self, placeName, description, location, rating, place_id = None):
        self.placeName = placeName
        self.description = description
        self.location = location
        self.rating = rating
        self.place_id = place_id
    
    def toQuery(self):
        query = {"placeName": self.placeName, "description": self.description, "location": self.location, "rating": self.rating}
        return query