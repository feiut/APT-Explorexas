class Report:

    def __init__(self, reportId, userId, placeId, categoryId, imgPath, imgId, review, rating):
        self.reportId = reportId
        self.userId = userId
        self.placeId = placeId
        self.categoryId = categoryId
        self.imgPath = imgPath
        self.imgId = imgId
        self.review = review
        self.rating = rating

    def toQuery(self):
        query = {"reportId": self.reportId, "userId": self.userId, "placeId": self.placeId, "categoryId": self.categoryId,
                 "imgPath": self.imgPath, "imgId": self.imgId, "review": self.review, "rating": self.rating}
        return query