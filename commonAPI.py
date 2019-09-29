
def connect_to_database(collection):
    import pymongo
    from pymongo import MongoClient

    client = pymongo.MongoClient(
        'mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/test?retryWrites=true&w=majority')
    db = client.test
    db = client['Explorexas']
    users = db[collection]
    return users