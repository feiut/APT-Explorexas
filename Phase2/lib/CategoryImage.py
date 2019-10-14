class CategoryImage:

    def __init__(self, imgData, imgId, userId):
        self.imgData = imgData
        self.imgId = imgId
        self.userId = userId

    def toQuery(self):
        query = {"imgData": self.imgData, "imgId": self.imgId, "userId": self.userId}
        return query