from lib import Report
from lib import ImageAPI
from lib import TagAPI
from lib import UserAPI
from lib import CategoryAPI
import pymongo

COLLECTION_NAME = "Reports"

class ReportAPI():
    def __init__(self):
        # self.client = pymongo.MongoClient("mongodb+srv://fei:20190101@cluster0-37xwl.mongodb.net/test?retryWrites=true&w=majority")
        self.client = pymongo.MongoClient("mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
        self.db = self.client['Explorexas']
        self.collection = self.db[COLLECTION_NAME]

    def add_report(self, report, image):
        # reportId, userId, placeId, categoryId, imgPath, imgId, tagId, review, rating
        reports = self.collection
        query = {'reportId': report.reportId}
        if reports.find_one(query):  # Report ID should be unique
            print("Report exist.")
            return False
        new_report = report.toQuery()
        imageapi = ImageAPI.ImageAPI()
        imageapi.add_image(image)
        result = reports.insert_one(new_report)
        print("Report created successfully.")
        return result

    def find_by_reportId(self, reportId):
        reports = self.collection
        query = {'reportId': reportId}
        try:
            result = reports.find_one(query)
        except:
            raise ValueError("Report not found!")
        report = Report.Report(result["reportId"],
                               result["userId"],
                               result["placeName"],
                               result["coordinates"],
                               result["categoryId"],
                               result["imgId"],
                               result["review"],
                               result["rating"],
                               result["timeStamp"])
        return report.toQuery()

    def delete_by_id(self, reportId):
        reports = self.collection
        query = {'reportId': reportId}
        report = reports.find_one(query)
        if not report:
            print("No report found")
            return False
        imageapi = ImageAPI.ImageAPI()
        imageapi.delete_image_by_id(report['imgId'])
        result = reports.delete_one({"reportId": reportId})
        return result

    def find_by_userId(self, userId):
        reports = self.collection
        query = {'userId': userId}
        if not reports.find_one(query):
            print("No report for userId:" + str(userId) + " was found")
            return None
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report.Report(result["reportId"],
                            result["userId"],
                            result["placeName"],
                            result["coordinates"],
                            result["categoryId"],
                            result["imgId"],
                            result["review"],
                            result["rating"],
                            result["timeStamp"])
            report_list.append(report)
        return report_list

    def find_reports_by_catId(self, catId):
        reports = self.collection
        query = {'categoryId': catId}
        if not reports.find_one(query):
            raise ValueError("Report not found!")
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report.Report(result["reportId"],
                            result["userId"],
                            result["placeName"],
                            result["coordinates"],
                            result["categoryId"],
                            result["imgId"],
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
        reportList = self.find_reports_by_catId(catId)
        for report in reportList:
            userName = userAPI.get(report.userId).userName
            catName = catAPI.get(catId).catName
            tagId = imageAPI.get_image_by_id(report.imgId).tagId
            tagName = tagAPI.get(tagId)
            reportContent = {"userName": userName, "placeName": report.placeName, 
                             "coordinates": report.coordinates, "categoryName": catName,
                             "imgId": report.imgId, "review": report.review, 
                             "rating": report.rating, "tagName":tagName,
                             "timeStamp": report.timeStamp}
            reportContentList.append(reportContent)
        return reportContentList