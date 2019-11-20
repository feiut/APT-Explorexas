import gridfs
from bson.objectid import ObjectId
import pymongo
from datetime import datetime 

DATABASE_NAME = "Explorexas"

class ImageAPI():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client[DATABASE_NAME]

    def add_image(self, image):
        fs = gridfs.GridFS(self.db)
        # TODO some image data don't have filename attribute

        result = fs.put(image.imgData, 
                        content_type='jpg', 
                        imgName=str(datetime.now()),
                        userId=image.userId)
        return result

    def get_image_by_id(self, imgId):
        fs = gridfs.GridFS(self.db)
        print("get by imgid")
        print(imgId)
        try:
            gridout = fs.get( ObjectId(imgId))
            return gridout
        except ValueError as exc:
            error_message = str(exc)
            raise ValueError(error_message)
        return False

    ##def get_image_by_tagId(self, tagId):
    ##    query = {'tagId': tagId}
    ##    if not self.db.fs.files.find_one(query):
    ##        print("Image not found")
    ##        return None
    ##    return self.db.fs.files.find(query)

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

    def close_connection(self):
        self.client.close()