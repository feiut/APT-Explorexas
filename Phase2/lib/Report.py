class Report:

    def __init__(self, 
                reportId, 
                userId, 
                title,
                placeName, 
                coordinates, 
                categoryId, 
                imgId, 
                review, 
                rating, 
                timeStamp):
        self._id = reportId
        self.userId = userId
        self.title = title
        self.placeName = placeName
        self.coordinates = coordinates
        self.categoryId = categoryId
        self.imgId = imgId
        self.review = review
        self.rating = rating
        self.timeStamp = timeStamp

    def toQuery(self):
        query = {
                "_id": self._id, 
                "userId": self.userId, 
                "title": self.title, 
                "placeName": self.placeName, 
                "coordinates": self.coordinates, 
                "categoryId": self.categoryId,
                "imgId": self.imgId, 
                "review": self.review, 
                "rating": self.rating, 
                "timeStamp": self.timeStamp
                 }
        return query