from bson.objectid import ObjectId
from lib import Tag
import pymongo
import re

COLLECTION_NAME = "Tags"

class TagAPI():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[COLLECTION_NAME]

    #[input]  tag object
    #[return] _id of inserted tag
    def insert(self, tag):
        collection = self.collection
        srchRlt = collection.find_one(tag.toQuery())
        if srchRlt is None:
            tag_id = collection.insert_one(tag.toQuery()).inserted_id
        else:
            tag_id = srchRlt['_id']
        return tag_id

    #[input]  tag object
    #[return] updated result
    def update(self, tag):
        collection = self.collection
        if tag.tag_id is None:
            print("Tag ID cannot be None")
            return None
        elif collection.find_one({"_id": ObjectId(tag.tag_id)}) is None:
            print("Tag ID does not exist, please create new tag instead")
            return None
        else:
            return collection.update_one({ "_id": ObjectId(tag.tag_id)}, {'$set':tag.toQuery()})

    #[input]  tag id
    #[return] tag object
    def get(self, tag_id):
        collection = self.collection
        srchRlt = collection.find_one({"_id": ObjectId(tag_id)})
        if srchRlt == None:
            print("The Tag corresponding the input tag id does not exist")
            return None
        else:
            tag = Tag.Tag(srchRlt["tagName"], srchRlt["_id"])
            return tag

    #[input]  None
    #[return] list of tag object
    def list(self):
        collection = self.collection
        results = collection.find({})
        tags = []
        for result in results:
            tag = Tag.Tag(result["tagName"], result["_id"])
            tags.append(tag)
        return tags

    #[input]  tag id
    #[return] deleted result
    def delete(self, tag_id):
        collection = self.collection
        srchRlt = collection.find_one({"_id": ObjectId(tag_id)})
        if srchRlt is None:
            print("The Tag corresponding the input tag id does not exist")
            return None
        else:
            result = collection.delete_one({"_id": ObjectId(tag_id)})
            return result

    #[input] tag string
    #[return] a list of tag id
    def srch_tagId_by_pattern(self, pattern):
        ptn = re.compile(pattern)
        tagList = self.list()
        tagIdList = []
        for tag in tagList:
            match = ptn.search(tag.tagName)
            if match:
                tagIdList.append(tag.tag_id)
        return tagIdList



