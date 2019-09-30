class Tag:

    def __init__(self, tagName, tag_id=None):
        self.tagName = tagName
        self.tag_id = tag_id

    def toQuery(self):
        query = {"tagName": self.tagName}
        return query