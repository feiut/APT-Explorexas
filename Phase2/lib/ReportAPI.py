from lib import Report
from lib import ImageAPI
from lib import TagAPI
from lib import UserAPI
from lib import CategoryAPI
from bson.objectid import ObjectId
import pymongo

COLLECTION_NAME = "Reports"

class ReportAPI():
    def __init__(self):
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[COLLECTION_NAME]

    def get_report_list(self):
        userAPI = UserAPI.UserAPI()
        catAPI = CategoryAPI.CategoryAPI()
        tagAPI = TagAPI.TagAPI()
        results = self.collection.find({})
        report_list = []
        for result in results:
            userName = userAPI.get(result['userId']).userName
            catName = catAPI.get(result['categoryId']).catName
            tagName = tagAPI.get(result['tagId']).tagName
            reportContent = {"reportId": str(result['_id']),
                             "userId": str(result['userId']),
                             "categoryId": str(result['categoryId']),
                             "tagId": str(result['tagId']),
                             "userName": userName,
                             "placeName": result['placeName'],
                             "coordinates": result['coordinates'],
                             "latitude": result['coordinates'][0],
                             "longitude": result['coordinates'][1],
                             "categoryName": catName,
                             "imgId": str(result['imgId']),
                             "tag": tagName,
                             "review": result['review'],
                             "rating": str(result['rating']),
                             "timeStamp": str(result['timeStamp']),
                             "title": result['title']}
            report_list.append(reportContent)
            # rep = Report.Report(result["_id"],
            #                     result["userId"],
            #                     result["title"],
            #                     result["placeName"],
            #                     result["coordinates"],
            #                     result["categoryId"],
            #                     result["imgId"],
            #                     result["tagId"],
            #                     result["review"],
            #                     result["rating"],
            #                     result["timeStamp"])
            # report_list.append(rep)
        return report_list

    def add_report(self, report):
        # reportId, userId, placeId, categoryId, imgPath, imgId, tagId, review, rating
        reports = self.collection
        new_report = report.toQuery()
        rptId = reports.insert_one(new_report)
        print("Report created successfully.")
        return rptId


    def update_cat_id(self, reportId, newCatId):
        reports = self.collection
        query = {'_id': reportId}
        result = reports.update_one( query , {"$set": {"categoryId": newCatId}})
        return result


    def find_by_reportId(self, reportId):
        reports = self.collection
        query = {'_id': ObjectId(reportId)}
        try:
            result = reports.find_one(query)
        except ValueError as exc:
            raise ValueError(str(exc))
        if result == None:
            print(query)
            raise ValueError("Report not found!")
        report = Report.Report(result["_id"],
                               result["userId"],
                               result["title"],
                               result["placeName"],
                               result["coordinates"],
                               result["categoryId"],
                               result["imgId"],
                               result["tagId"],
                               result["review"],
                               result["rating"],
                               result["timeStamp"])
        return report.toQuery()

    def delete_by_id(self, reportId):
        reports = self.collection
        query = {'_id': reportId}
        report = reports.find_one(query)
        if not report:
            print("No report found")
            return False
        imageapi = ImageAPI.ImageAPI()
        imageapi.delete_image_by_id(report['imgId'])
        result = reports.delete_one({"_id": reportId})
        return result

    def mobile_find_by_userId(self, userId):
        reports = self.collection
        query = {'userId': userId}
        results = reports.find(query)
        reportList = []
        tagAPI = TagAPI.TagAPI()
        userAPI = UserAPI.UserAPI()
        catAPI = CategoryAPI.CategoryAPI()
        for report in results:
            userName = userAPI.get(userId).userName
            catName = catAPI.get(report['categoryId']).catName
            tagName = tagAPI.get(report['tagId']).tagName
            reportContent = {"reportId": str(report['_id']),
                             "userId": userId,
                             "userName": userName,
                             "placeName": report['placeName'],
                             "coordinates": report['coordinates'],
                             "categoryName": catName,
                             "imgId": str(report['imgId']),
                             "tag": tagName,
                             "review": report['review'],
                             "rating": report['rating'],
                             "timeStamp": report['timeStamp'],
                             "title": report['title']}
            reportList.append(reportContent)
        return reportList

    def find_by_userId(self, userId):
        reports = self.collection
        query = {'userId': userId}
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report.Report(ObjectId(result["_id"]),
                            result["userId"],
                            result["title"],
                            result["placeName"],
                            result["coordinates"],
                            result["categoryId"],
                            result["imgId"],
                            result["tagId"],
                            result["review"],
                            result["rating"],
                            result["timeStamp"])
            report_list.append(report)
        return report_list

    def find_by_catId(self, catId):
        reports = self.collection
        query = {'categoryId': ObjectId(catId)}
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report.Report(result["_id"],
                            result["userId"],
                            result["title"],
                            result["placeName"],
                            result["coordinates"],
                            result["categoryId"],
                            result["imgId"],
                            result["tagId"],
                            result["review"],
                            result["rating"],
                            result["timeStamp"])
            report_list.append(report)
        return report_list

    def find_by_tagId(self, tagId):
        reports = self.collection
        query = {'tagId': tagId}
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report.Report(result["_id"],
                            result["userId"],
                            result["title"],
                            result["placeName"],
                            result["coordinates"],
                            result["categoryId"],
                            result["imgId"],
                            result["tagId"],
                            result["review"],
                            result["rating"],
                            result["timeStamp"])
            report_list.append(report)
        return report_list


    def get_report_content_list_by_catId(self, catId): 
        imageAPI = ImageAPI.ImageAPI()
        tagAPI = TagAPI.TagAPI()
        userAPI = UserAPI.UserAPI()
        catAPI = CategoryAPI.CategoryAPI()
        reportContentList = []
        reportList = self.find_by_catId(catId)
        if len(reportList) > 0:
            for report in reportList:
                userName = userAPI.get(report.userId).userName
                catName = catAPI.get(catId).catName
                tagName = tagAPI.get(report.tagId).tagName
                reportContent = {"reportId": str(report.reportId),
                                "userId": report.userId, 
                                 "userName": userName, 
                                 "placeName": report.placeName, 
                                 "coordinates": report.coordinates, 
                                 "categoryName": catName,
                                 "imgId": str(report.imgId),
                                 "tag": tagName, 
                                 "review": report.review, 
                                 "rating": report.rating, 
                                 "timeStamp": report.timeStamp, 
                                 "title":report.title}
                reportContentList.append(reportContent)
        return reportContentList

    def get_report_content_list_by_tagId(self, tagId):
        userAPI = UserAPI.UserAPI()
        catAPI = CategoryAPI.CategoryAPI()
        tagAPI = TagAPI.TagAPI()

        reportContentList = []
        reportList = self.find_by_tagId(tagId)
        if len(reportList) > 0:
            for report in reportList:
                userName = userAPI.get(report.userId).userName
                catName = catAPI.get(report.categoryId).catName
                tagName = tagAPI.get(tagId).tagName
                reportContent = {"reportId": str(report.reportId),
                                 "userName": userName, 
                                 "placeName": report.placeName, 
                                 "coordinates": report.coordinates, 
                                 "categoryName": catName,
                                 "imgId": str(report.imgId),
                                 "tag": tagName, 
                                 "review": report.review, 
                                 "rating": report.rating, 
                                 "timeStamp": report.timeStamp, 
                                 "title":report.title}
                reportContentList.append(reportContent)
            return reportContentList
        else:
            return None

    def list_by_userId(self, userIds):
        results = self.collection.find({'userId': {'$in': userIds}})
        report_list = []
        userAPI = UserAPI.UserAPI()
        catAPI = CategoryAPI.CategoryAPI()
        tagAPI = TagAPI.TagAPI()
        for result in results:
            userName = userAPI.get(result["userId"]).userName
            catName = catAPI.get(result["categoryId"]).catName
            tagName = tagAPI.get(result["tagId"]).tagName
            report = {
                        "reportId": str(result["_id"]),
                        "userId": result["userId"],
                        "userName": userName,
                        "title": result["title"],
                        "placeName": result["placeName"],
                        "coordinates": result["coordinates"],
                        "categoryId": str(result["categoryId"]),
                        "categoryName": catName,
                        "imgId": str(result["imgId"]),
                        "tag": tagName,
                        "tagId": str(result["tagId"]),
                        "review": result["review"],
                        "rating": result["rating"],
                        "timeStamp": result["timeStamp"]
                    }

            report_list.append(report)
        return report_list
            
    def close_connection(self):
        self.client.close()