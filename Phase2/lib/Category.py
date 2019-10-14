class Category:
    def __init__(self, catName, catDescription, imgId = 'default' , userId = 'default', cat_id = None):
        self.catName = catName
        self.catDescription = catDescription
        self.imgId = imgId
        self.userId = userId
        self.cat_id = cat_id

    def toQuery(self):
        query = {"catName": self.catName, "catDescription": self.catDescription, "imgId": self.imgId, "userId": self.userId}
        return query