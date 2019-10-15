import gridfs
from bson.objectid import ObjectId
import pymongo

DATABASE_NAME = "Images"

class ImageAPI():
    def __init__(self):
        # self.client = pymongo.MongoClient("mongodb+srv://fei:20190101@cluster0-37xwl.mongodb.net/test?retryWrites=true&w=majority")
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client[DATABASE_NAME]

    def add_image(self, image):
        # imgPath, imgId, reportId, userId, tagId
        query = {'_id': image.imgId}
        # if self.db.fs.files.find_one(query):  # Image ID need to be different 
        #     print("image exist")
        #     return False
        fs = gridfs.GridFS(self.db)
        f = image.imgData.filename.split('.')
        result = fs.put(image.imgData, 
                        content_type=f[1], 
                        imgName=f[0], 
                        _id=image.imgId,
                        reportId=image.reportId, 
                        userId=image.userId, 
                        tagId=image.tagId)
        return result

    def get_image_by_id(self, imgId):
        # query = {'_id': imgId}
        fs = gridfs.GridFS(self.db)
        # if not self.db.fs.files.find_one(query):
        try:
            gridout = fs.get_last_version(_id = imgId)
        except:
            raise ValueError('No image found!')
        if not gridout:
            raise ValueError('No image found!')
        # return self.db.fs.files.find(query)
        return gridout

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