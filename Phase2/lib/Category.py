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
        
    def toJSON(self):
        return {
            'catName': self.catName, 
            'catDescription': self.catDescription,
            'imageId': str(self.imageId),
            'userId': str(self.userId),
            'cat_id': str(self.cat_id)
        }