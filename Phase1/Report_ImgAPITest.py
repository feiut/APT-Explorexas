from ReportAPI import ReportAPI
from Report import Report
from ImageAPI import ImageAPI
from Image import Image

def testPlaceAPI():

    # Report(reportId, userId, placeId, categoryId, imgPath, imgId, review, rating)
    # Image(imgPath, imgId, reportId, userId, tagId)
    report0 = Report(999, 1, 77, 10, "testImg.jpg", 9999, "Nice place!", 5)
    image0 = Image(report0.imgPath, report0.imgId, report0.reportId, report0.userId, 998)

    controllerReport = ReportAPI()
    # controllerImage = ImageAPI()

    print("Test add report")
    result = controllerReport.add_report(report0, image0)
    assert(result is not None)
    print("Passed")

    print("Test find report by userID")
    results = controllerReport.find_reports_by_userId(report0.userId)
    for result in results:
        assert(result.userId == report0.userId)
    print("Passed")

    print("Test delete report")
    controllerReport.delete_report_by_id(report0.reportId)
    results = controllerReport.find_reports_by_userId(report0.reportId)
    assert(results == None)
    print("Passed")

def testImageAPI():

    report1 = Report(990, 2, 77, 10, "testImg.jpg", 9997, "Nice place!", 5)
    image1 = Image(report1.imgPath, report1.imgId, report1.reportId, report1.userId, 997)

    controllerImage = ImageAPI()

    print("Test add image")
    result = controllerImage.add_image(image1)
    assert(result is not None)
    print("Passed")

    print("Test get image by id")
    results = controllerImage.get_image_by_id(image1.imgId)
    for result in results:
        assert(result['_id'] == image1.imgId)
    print("Passed")

    print("Test get image by tagId")
    results = controllerImage.get_image_by_tagId(image1.tagId)
    for result in results:
        assert(result['tagId'] == image1.tagId)
    print("Passed")

    print("Test delete image by imgid")
    controllerImage.delete_image_by_id(image1.imgId)
    results = controllerImage.get_image_by_id(image1.imgId)
    assert (results == None)
    print("Passed")