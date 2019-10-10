class Category:
    def __init__(self, catName, catDescription, pic, cat_id = None):
        self.catName = catName
        self.catDescription = catDescription
        self.pic = pic
        self.cat_id = cat_id

    def toQuery(self):
        query = {"catName": self.catName, "catDescription": self.catDescription, "pic": self.pic}
        return query