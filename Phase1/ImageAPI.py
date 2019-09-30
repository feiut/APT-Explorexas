import gridfs
from utils import get_imagedb

class ImageAPI():

    def add_image(self, image):
        # imgPath, imgId, reportId, userId, tagId
        db = get_imagedb()
        query = {'_id': image.imgId}
        if db.fs.files.find_one(query):
            print("image exist")
            return False
        imgput = gridfs.GridFS(db)
        datatmp = open(image.imgPath, 'rb')
        f = image.imgPath.split('.')
        result = imgput.put(datatmp, content_type=f[1], imgName=f[0], _id=image.imgId, \
                               reportId=image.reportId, userId=image.userId, tagId=image.tagId)
        datatmp.close()
        return result

    def get_image_by_id(self, imgId):
        db = get_imagedb()
        query = {'_id': imgId}
        if not db.fs.files.find_one(query):
            print("Image not found")
            return None
        return db.fs.files.find(query)

    def get_image_by_tagId(self, tagId):
        db = get_imagedb()
        query = {'tagId': tagId}
        if not db.fs.files.find_one(query):
            print("Image not found")
            return None
        return db.fs.files.find(query)

    def delete_image_by_id(self, imgId):
        db = get_imagedb()
        query = {'_id': imgId}
        result = db.fs.files.find_one(query)
        if not result:
            print("Image not found")
            return False
    # use the _id to delete the file
        files_id = result['_id']
        fs = gridfs.GridFS(db)
        result = fs.delete(files_id)
        return result