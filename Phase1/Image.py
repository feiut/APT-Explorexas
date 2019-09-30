class Image:

    def __init__(self, imgPath, imgId, reportId, userId, tagId):
        self.imgPath = imgPath
        self.imgId = imgId
        self.reportId = reportId
        self.userId = userId
        self.tagId = tagId

    def toQuery(self):
        query = {"imgPath": self.imgPath, "imgId": self.imgId, "reportId": self.reportId, "userId": self.userId,
                 "tagId": self.tagId}
        return query