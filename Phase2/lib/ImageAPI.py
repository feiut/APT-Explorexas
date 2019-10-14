import gridfs
from bson.objectid import ObjectId
import pymongo

DATABASE_NAME = "Images"

class ImageAPI():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Images']
        self.collection = self.db['what?']
        self.collection.insert_one({"what": "what?"})

    def add_image(self, image):
        # imgPath, imgId, reportId, userId, tagId
        query = {'_id': image.imgId}
        if self.db.fs.files.find_one(query):
            print("image exist")
            return False
        imgput = gridfs.GridFS(self.db)
        f = image.imgData.filename.split('.')
        result = imgput.put(image.imgData, content_type=f[1], imgName=f[0], _id=image.imgId, \
                               reportId=image.reportId, userId=image.userId, tagId=image.tagId)
        return result

    def get_image_by_id(self, imgId):
        query = {'_id': imgId}
        if not self.db.fs.files.find_one(query):
            print("Image not found")
            return None
        return self.db.fs.files.find(query)

    def get_image_by_tagId(self, tagId):
        query = {'tagId': tagId}
        if not self.db.fs.files.find_one(query):
            print("Image not found")
            return None
        return self.db.fs.files.find(query)

    def delete_image_by_id(self, imgId):
        query = {'_id': imgId}
        result = self.db.fs.files.find_one(query)
        if not result:
            print("Image not found")
            return False
    # use the _id to delete the file
        files_id = result['_id']
        fs = gridfs.GridFS(self.db)
        result = fs.delete(files_id)
        return result