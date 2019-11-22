class User:
    def __init__(self, userId, userName, subscription = None):
        self.userId = userId
        self.userName = userName
        if subscription is None: subscription = []
        self.subscription = subscription

    def toQuery(self):
        subscription = "[]"
        query = {"userId": self.userId, "userName": self.userName, "subscription": self.subscription}
        return query