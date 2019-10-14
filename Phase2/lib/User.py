class User:
    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName

    def toQuery(self):
        query = {"userId": self.userId, "userName": self.userName}
        return query