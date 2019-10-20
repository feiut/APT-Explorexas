from flask import Flask, render_template, request, redirect, url_for
from google.auth.transport import requests
from google.cloud import datastore
from datetime import datetime 
import google.oauth2.id_token
import uuid
from bson.objectid import ObjectId
from lib import Category, CategoryAPI, CategoryImage, CategoryImageAPI
from lib import Report, ReportAPI
from lib import Image, ImageAPI
from lib import User, UserAPI
from lib import Tag, TagAPI
from flask import make_response

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()
claims = None

@app.route('/createCategory')
def createCategory():
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            controller = CategoryAPI.CategoryAPI()
            insert_result = controller.list_user_creation(claims["email"])
        except ValueError as exc:
            return render_template('noLogin.html')
        controller.close_connection()
        return render_template('createCategory.html', inserted_data=insert_result, user_data=claims)
    return render_template('noLogin.html')


@app.route('/deleteCategory', methods=['POST'])
def deleteCategory():
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            controller = CategoryAPI.CategoryAPI()
            othersId = controller.get_cat_Id_by_name("Others")
            repController = ReportAPI.ReportAPI()
            categoryReports = repController.find_by_catId(request.form['categoryId'])
            for report in categoryReports:
                result = repController.update_cat_id(report.reportId, othersId)
            delete_result = controller.delete_by_id(request.form['categoryId'])
            insert_result = controller.list_user_creation(claims["email"])
        except ValueError as exc:
            return render_template('noLogin.html')
        controller.close_connection()
        return render_template('createCategory.html', inserted_data=insert_result, user_data=claims)
    return render_template('noLogin.html')


@app.route('/create_category', methods=['POST'])
def create_category():
    categoryName = request.form['categoryName']
    categoryDescription = request.form['categoryDescription']
    pic = request.files['file']
    userId = request.form['userId']
    # imgId = request.form['imgId']
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            controller = CategoryAPI.CategoryAPI()
            imageController = ImageAPI.ImageAPI()
            image = Image.Image(imgData=pic, userId=userId)
            imageId = imageController.add_image(image)
            findExistingOne = controller.get_cat_by_name(categoryName)
            if findExistingOne == None:
                cat = Category.Category(categoryName, categoryDescription, imageId, userId)
                insert_id = controller.insert(cat)
                insert_result = controller.list_user_creation(userId)
                error_message = None
            else:
                error_message = "Sorry, this category has already existed."
                insert_result = controller.list_user_creation(userId)
        except ValueError as exc:
            error_message = str(exc)
    controller.close_connection()
    return render_template(
            'createCategory.html', inserted_data=insert_result, user_data=claims, error = error_message)


@app.route('/create_report', methods=['POST'])
def create_report():
    # Report ID and Image ID need to be unique
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            userId = claims['email']            
            title = request.form['title']
            placeName = request.form['placeName']
            latitude = request.form['latitude']
            longitude = request.form['longitude']
            coordinates = [latitude, longitude]
            categoryName = request.form['categoryName']
            catController = CategoryAPI.CategoryAPI()
            categoryId = catController.get_cat_by_name(categoryName).cat_id
            review = request.form['review']
            rating = request.form['rating']
            timeStamp = datetime.now()
            tagName = request.form['tagName']
            tag = Tag.Tag(tagName)
            tagController = TagAPI.TagAPI()
            tagId = tagController.insert(tag)
            pic = request.files['file']
            imgId = ObjectId()
            repController = ReportAPI.ReportAPI()
            report = Report.Report( None,
                                    userId, 
                                    title, 
                                    placeName, 
                                    coordinates,  
                                    categoryId, 
                                    imgId,
                                    tagId, 
                                    review, 
                                    rating, 
                                    timeStamp)
            # image = Image.Image(pic, imgId, userId)
            image = Image.Image(pic, userId)
            inserted_id = repController.add_report(report, image).inserted_id
            reportDisplay = repController.find_by_reportId(inserted_id)
            # to display tag name instead of tag id in reports.html
            reportDisplay["tagId"] = tagController.get(reportDisplay["tagId"]).tagName
            # print(report["imgId"])
            return render_template('reports.html', report=reportDisplay, imgId=reportDisplay["imgId"])
        except ValueError as exc:
            error_message = str(exc)
    return render_template('nologin.html')

@app.route('/createReport')
def createReport():
    id_token = request.cookies.get("token")
    catController = CategoryAPI.CategoryAPI()
    catList = []
    for cat in catController.list():
        catList.append(cat.toQuery())
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        except ValueError as exc:
            return render_template('noLogin.html')
        catController.close_connection()
        return render_template('createReport.html', catList=catList)
    else:
        return render_template('noLogin.html')

@app.route('/images/<imgId>')
def image(imgId):
    imgController = ImageAPI.ImageAPI()
    image = imgController.get_image_by_id(imgId)
    response = make_response(image.read())
    response.mimetype = 'image/jpeg'
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % imgId)
    return response
    return redirect(url_for('createReport'))
    
@app.route('/reports/<reportId>')
def report(reportId):
    repController = ReportAPI.ReportAPI()
    imgController = ImageAPI.ImageAPI()
    catController = CategoryAPI.CategoryAPI()
    report = repController.find_by_reportId(reportId)
    categoryName = catController.get(report["categoryId"]).catName
    return render_template('reports.html', report=report, imgId=report["imgId"], categoryName= categoryName)

@app.route('/viewCategoryPost/<catId>')
def viewCategoryPost(catId):
    repController = ReportAPI.ReportAPI()
    catController = CategoryAPI.CategoryAPI()
    reportContentList = repController.get_report_content_list_by_catId(catId)
    categoryName = catController.get(catId).catName
    if len(reportContentList):
        reportContentList.sort(key=lambda rpt:rpt["timeStamp"], reverse=True)
    return render_template('viewCategoryPost.html', 
        reportContentList=reportContentList, 
        categoryName=categoryName)

@app.route('/searchTag', methods=['POST'])
def searchTag():
    pattern = request.form['searchTag']
    tagController = TagAPI.TagAPI()
    repController = ReportAPI.ReportAPI()

    tagIdList = tagController.srch_tagId_by_pattern(pattern)
    if len(tagIdList):
        currRptContentList = []
        for tagId in tagIdList:
            rptContentList = repController.get_report_content_list_by_tagId(tagId)
            currRptContentList.extend(rptContentList)
        currRptContentList.sort(key=lambda rpt:rpt["timeStamp"], reverse=True)
        return render_template('viewTagPost.html', reportContentList=currRptContentList)
    else:
        return render_template('noMatchRlt.html')

# @app.route('/user_reports/<userId>') 
# def report(userId):
#     repController = ReportAPI.ReportAPI()
#     imgController = ImageAPI.ImageAPI()
#     reports = repController.find_reports_by_userId(userId)
#     return render_template('reports.html', imgId=1)

@app.route('/login')
def login():
    return render_template('login.html', now = str(datetime.utcnow()))

@app.route('/welcomePage')
def welcomePage():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user = User.User(claims["email"], claims["name"])
            user_controller = UserAPI.UserAPI()
            search_user = user_controller.insert(user)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template(
        'welcome.html',
        user_data=claims, error_message=error_message, now = str(datetime.utcnow()))

@app.route('/')
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None

    if id_token:
        try:
            # Verify the token against the Firebase Auth API. This example
            # verifies the token on each page load. For improved performance,
            # some applications may wish to cache results in an encrypted
            # session store (see for instance
            # http://flask.pocoo.org/docs/1.0/quickstart/#sessions).
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            user = User.User(claims["email"], claims["name"])
            user_controller = UserAPI.UserAPI()
            search_user = user_controller.insert(user)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    categoryContrller = CategoryAPI.CategoryAPI()
    categories = categoryContrller.list()

    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, categories=categories, now = str(datetime.utcnow()))


# Connect to MongoDB database
# def get_db_collection():
#     client = pymongo.MongoClient(
#         "mongodb+srv://admin-user01:19961106@cluster0-eteyg.mongodb.net/admin?retryWrites=true&w=majority")
#     db = client.Explorexas
#     cluster = db.Categories
#     return cluster


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=3000, debug=True)
    # db = get_db_collection()
