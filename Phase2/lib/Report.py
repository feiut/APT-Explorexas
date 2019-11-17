class Report:

    def __init__(self, 
                reportId, 
                userId, 
                title,
                placeName, 
                coordinates, 
                categoryId, 
                imgId,
                tagId, 
                review, 
                rating, 
                timeStamp):
        self.reportId = reportId
        self.userId = userId
        self.title = title
        self.placeName = placeName
        self.coordinates = coordinates
        self.categoryId = categoryId
        self.imgId = imgId
        self.tagId = tagId
        self.review = review
        self.rating = rating
        self.timeStamp = timeStamp

    def toQuery(self):
        query = {
                "userId": self.userId, 
                "title": self.title, 
                "placeName": self.placeName,
                "coordinates": self.coordinates, 
                "categoryId": self.categoryId,
                "imgId": self.imgId,
                "tagId": self.tagId, 
                "review": self.review, 
                "rating": self.rating, 
                "timeStamp": self.timeStamp
                 }
        return query

    def toJSON(self):
        return {
            "reportId": str(self.reportId),
            "userId": str(self.userId),
            "title": self.title,
            "placeName": self.placeName,
            "coordinates": self.coordinates,
            "latitude": self.coordinates[0],
            "longitude": self.coordinates[1],
            "categoryId": str(self.categoryId),
            "imgId": str(self.imgId),
            "tagId": str(self.tagId),
            "review": self.review,
            "rating": str(self.rating),
            "timeStamp": str(self.timeStamp)
        }