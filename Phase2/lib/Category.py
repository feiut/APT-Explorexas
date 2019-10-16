class Category:
    def __init__(self, catName, catDescription, imageId='default', userId = 'default', cat_id = None):
        self.catName = catName
        self.catDescription = catDescription
        self.imageId = imageId
        self.userId = userId
        self.cat_id = cat_id

    def toQuery(self):
        query = {"catName": self.catName, "catDescription": self.catDescription, "imageId" : self.imageId, "userId": self.userId}
        return query