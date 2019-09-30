from Report import Report
from ImageAPI import ImageAPI
from utils import get_db_collection

class ReportAPI():

    def add_report(self, report, image):
        # reportId, userId, placeId, categoryId, imgPath, imgId, tagId, review, rating
        reports = get_db_collection('Reports')
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
        reports = get_db_collection('Reports')
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
        reports = get_db_collection('Reports')
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