class Image:

    def __init__(self, imgData, imgId, reportId, userId, tagId):
        self.imgData = imgData
        self.imgId = imgId
        self.reportId = reportId
        self.userId = userId
        self.tagId = tagId

    def toQuery(self):
        query = {"imgData": self.imgData, "imgId": self.imgId, "reportId": self.reportId, "userId": self.userId,
                 "tagId": self.tagId}
        return query