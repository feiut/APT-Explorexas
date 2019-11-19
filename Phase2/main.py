from flask import Flask, render_template, request, redirect, url_for, jsonify 
from google.auth.transport import requests
from google.cloud import datastore
from datetime import datetime 
import google.oauth2.id_token
import os
import uuid
from bson.objectid import ObjectId
from lib import Category, CategoryAPI, CategoryImage, CategoryImageAPI
from lib import Report, ReportAPI
from lib import Image, ImageAPI
from lib import User, UserAPI
from lib import Tag, TagAPI
from flask import make_response
from werkzeug.datastructures import FileStorage
from flask_mobility import Mobility

app = Flask(__name__)
Mobility(app)
# datastore_client = datastore.Client()
# firebase_request_adapter = requests.Request()
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
            return render_template('nologin.html')
        controller.close_connection()
        return render_template('createCategory.html', inserted_data=insert_result, user_data=claims)
    return render_template('nologin.html')


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
            return render_template('nologin.html')
        controller.close_connection()
        return render_template('createCategory.html', inserted_data=insert_result, user_data=claims)
    return render_template('nologin.html')


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
            return render_template('nologin.html')
    controller.close_connection()
    return render_template(
            'createCategory.html', inserted_data=insert_result, user_data=claims, errors=error_message)


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
            imageController = ImageAPI.ImageAPI()
            image = Image.Image(pic, userId)
            imgId = imageController.add_image(image)
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
            reportId = repController.add_report(report).inserted_id
            reportDisplay = repController.find_by_reportId(reportId)
            # to display tag name instead of tag id in reports.html
            reportDisplay["tagId"] = tagController.get(reportDisplay["tagId"]).tagName
            catController = CategoryAPI.CategoryAPI()
            categoryName = catController.get(reportDisplay["categoryId"]).catName
            repController.close_connection()
            tagController.close_connection()
            catController.close_connection()
            reportDisplay["categoryId"] = categoryName
            return render_template('reports.html', report=reportDisplay, user_data=claims, imgId=reportDisplay["imgId"])
        except ValueError as exc:
            error_message = str(exc)
            print(error_message)
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
            return render_template('nologin.html')
        catController.close_connection()
        return render_template('createReport.html', user_data=claims, catList=catList)
    else:
        return render_template('nologin.html')


@app.route('/images/<imgId>')
def image(imgId):
    imgController = ImageAPI.ImageAPI()
    image = imgController.get_image_by_id(imgId)
    response = make_response(image.read())
    response.mimetype = 'image/jpeg'
    response.headers.set(
    'Content-Disposition', 'attachment', filename='%s.jpg' % imgId)
    return response


@app.route('/reports/<reportId>')
def report(reportId):
    id_token = request.cookies.get("token")
    claims = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        except ValueError as exc:
            print("Login info Error! : " + str(exc))
    repController = ReportAPI.ReportAPI()
    catController = CategoryAPI.CategoryAPI()
    tagController = TagAPI.TagAPI()
    reportDisplay = repController.find_by_reportId(reportId)
    categoryName = catController.get(reportDisplay["categoryId"]).catName
    reportDisplay["tagId"] = tagController.get(reportDisplay["tagId"]).tagName
    repController.close_connection()
    tagController.close_connection()
    catController.close_connection()
    reportDisplay["categoryId"] = categoryName
    return render_template('reports.html', report=reportDisplay, user_data=claims, imgId=reportDisplay["imgId"])


@app.route('/viewCategoryPost/<catId>')
def viewCategoryPost(catId):
    repController = ReportAPI.ReportAPI()
    catController = CategoryAPI.CategoryAPI()
    reportContentList = repController.get_report_content_list_by_catId(catId)
    categoryName = catController.get(catId).catName
    repController.close_connection()
    catController.close_connection()
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        except ValueError as exc:
            error_message = str(exc)
    if len(reportContentList):
        reportContentList.sort(key=lambda rpt:rpt["timeStamp"], reverse=True)

    if request.MOBILE == False:
        return render_template('viewCategoryPost.html', 
            reportContentList=reportContentList, 
            categoryName=categoryName, user_data=claims, error = error_message)
    else:
        return jsonify(reportContentList)


@app.route('/searchTag/<ptn>', methods=['POST', 'GET'])
def searchTag(ptn):
    if request.method == 'POST':
        pattern = request.form['searchTag']
        tagController = TagAPI.TagAPI()
        repController = ReportAPI.ReportAPI()
        tagIdList = tagController.srch_tagId_by_pattern(pattern)
        id_token = request.cookies.get("token")
        claims = None
        error_message = None
        if id_token:
            try:
                claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            except ValueError as exc:
                error_message = str(exc)

        if len(tagIdList):
            currRptContentList = []
            for tagId in tagIdList:
                rptContentList = repController.get_report_content_list_by_tagId(tagId)
                if rptContentList != None :
                    currRptContentList.extend(rptContentList)

            if len(currRptContentList) == 0:
                tagController.close_connection()
                repController.close_connection()
                if request.MOBILE == False:
                    return render_template('noMatchReport.html',
                                           user_data=claims, 
                                           error = error_message)
                else:
                    return jsonify([])
            else:
                currRptContentList.sort(key=lambda rpt: rpt["timeStamp"], reverse=True)
                tagController.close_connection()
                repController.close_connection()
                if request.MOBILE == False  :
                    return render_template('viewTagPost.html',
                                           reportContentList=currRptContentList,
                                           user_data=claims, 
                                           error = error_message)
                else:
                    return jsonify(currRptContentList)
        else:
            tagController.close_connection()
            repController.close_connection()
            if request.MOBILE == False:
                return render_template('noMatchRlt.html',
                                        user_data=claims, 
                                        error = error_message)
            else:
                return jsonify([])

    elif request.method == 'GET':
        pattern = ptn
        tagController = TagAPI.TagAPI()
        repController = ReportAPI.ReportAPI()
        tagIdList = tagController.srch_tagId_by_pattern(pattern)
        id_token = request.cookies.get("token")
        claims = None
        error_message = None
        if id_token:
            try:
                claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            except ValueError as exc:
                error_message = str(exc)

        if len(tagIdList):
            currRptContentList = []
            for tagId in tagIdList:
                rptContentList = repController.get_report_content_list_by_tagId(tagId)
                if rptContentList != None :
                    currRptContentList.extend(rptContentList)

            if len(currRptContentList) == 0:
                tagController.close_connection()
                repController.close_connection()
                if request.MOBILE == False:
                    return render_template('noMatchReport.html',
                                           user_data=claims, 
                                           error = error_message)
                else:
                    return jsonify([])
            else:
                currRptContentList.sort(key=lambda rpt: rpt["timeStamp"], reverse=True)
                tagController.close_connection()
                repController.close_connection()
                if request.MOBILE == False  :
                    return render_template('viewTagPost.html',
                                           reportContentList=currRptContentList,
                                           user_data=claims, 
                                           error = error_message)
                else:
                    return jsonify(currRptContentList)
        else:
            tagController.close_connection()
            repController.close_connection()
            if request.MOBILE == False:
                return render_template('noMatchRlt.html',
                                        user_data=claims, 
                                        error = error_message)
            else:
                return jsonify({})


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


@app.route('/profile')
def profile():
    id_token = request.cookies.get("token")
    user = None
    if id_token:
        claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
        user = User.User(claims["email"], claims["name"])
        if user is None:
            return login()
        else:
            repController = ReportAPI.ReportAPI()
            toDelete = ObjectId(request.args.get("delete"))
            print("Report id: ", toDelete)
            if toDelete != "":
                repController.delete_by_id(toDelete)
                print(toDelete, " is deleted.")
            reports = repController.find_by_userId(user.userId)
            reports.sort(key=lambda rpt:rpt.timeStamp, reverse=True)
            repController.close_connection()
            return render_template('profile.html', reports=reports, user_data=claims)


@app.route('/')
def desktop_root():
    return root(False)


@app.route('/mobile')
def mobile_root():
    return root(True)


def root(mobile):
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

    if mobile == False:
        return render_template(
        'index.html',
        user_data=claims, error_message=error_message, categories=categories, now = str(datetime.utcnow()))
    else:
        return jsonify([cat.toJSON() for cat in categories])


@app.route('/findReports')
def find_reports_for_map():
    rep_controller = ReportAPI.ReportAPI()
    reports = rep_controller.get_report_list()
    rep_controller.close_connection()
    return jsonify([rep for rep in reports])

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
