import pymongo
import configparser

config = configparser.ConfigParser()
config.read('app.ini')
connectionString = config['DEFAULT']['connectionString']

def get_db_collection(collection_name):
    client = pymongo.MongoClient(connectionString)
    db = client['Explorexas']
    return db[collection_name]

def get_imagedb():
    client = pymongo.MongoClient(connectionString)
    return client.images