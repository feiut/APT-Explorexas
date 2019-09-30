from pymongo import MongoClient
from Report import Report
from Image import Image
from ImageAPI import ImageAPI

class ReportAPI():

    def connect_to_database(self, collection):
        client = MongoClient("mongodb+srv://fei:20190101@cluster0-37xwl.mongodb.net/test?retryWrites=true&w=majority")
        #     client = MongoClient("mongodb+srv://feihe:19950214@cluster0-eteyg.mongodb.net/test?retryWrites=true&w=majority")
        db = client['Explorexas']
        target = db[collection]
        return target

    def add_report(self, report, image):
        # reportId, userId, placeId, categoryId, imgPath, imgId, tagId, review, rating
        reports = self.connect_to_database('Reports')
        query = {'reportId': report.reportId}
        if reports.find_one(query):
            print("Report exist.")
            return False
        new_report = report.toQuery()
        result = reports.insert_one(new_report)
        imageapi = ImageAPI()
        imageapi.add_image(image)
        print("Report created successfully.")
        return result

    def delete_report_by_id(self, reportId):
        reports = self.connect_to_database('Reports')
        query = {'reportId': reportId}
        report = reports.find_one(query)
        if not report:
            print("No report found")
            return False
        imageapi = ImageAPI()
        imageapi.delete_image_by_id(report['imgId'])
        result = reports.delete_one({"reportId": reportId})
        return result

    def find_reports_by_userId(self, userId):
        reports = self.connect_to_database('Reports')
        query = {'userId': userId}
        if not reports.find_one(query):
            print("No report for userId:" + str(userId) + " was found")
            return None
        results = reports.find(query)
        report_list = []
        for result in results:
            report = Report(result["reportId"],
                            result["userId"],
                            result["placeId"],
                            result["categoryId"],
                            result["imgPath"],
                            result["imgId"],
                            result["review"],
                            result["rating"])
            report_list.append(report)
        return report_list