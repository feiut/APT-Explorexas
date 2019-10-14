import gridfs
from bson.objectid import ObjectId
import pymongo

DATABASE_NAME = "CategoryImages"

class CategoryImageAPI():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[DATABASE_NAME]

    def add_image(self, image):
        # imgPath, imgId, userId
        query = {'_id': image.imgId}
        if self.db.fs.files.find_one(query):
            print("image exists")
            return False
        imgput = gridfs.GridFS(self.db)
        f = image.imgData.filename.split('.')
        result = imgput.put(image.imgData, content_type=f[1], imgName=f[0], _id=image.imgId, userId=image.userId)
        return result

    def get_image_by_id(self, imgId):
        query = {'_id': imgId}
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