class CategoryImage:

    def __init__(self, imgData, userId):
        self.imgData = imgData
        self.userId = userId

    def toQuery(self):
        query = {"imgData": self.imgData, "userId": self.userId}
        return query