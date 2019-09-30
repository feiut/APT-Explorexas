class Category:
    def __init__(self, catName, cat_id = None):
        self.catName = catName
        self.cat_id = cat_id

    def toQuery(self):
        query = {"catName": self.catName}
        return query