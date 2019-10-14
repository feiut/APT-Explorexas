from flask import Flask, render_template, request, redirect, url_for
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from lib import Category, CategoryAPI, CategoryImage, CategoryImageAPI
from lib import Report, ReportAPI
from lib import Image, ImageAPI
from lib import User, UserAPI


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
            for result in insert_result:
                print(result)
        except ValueError as exc:
            error_message = str(exc)
    return render_template('createCategory.html', inserted_data=insert_result, user_data=claims)


@app.route('/createReport')
def createReport():
    return render_template('createReport.html')


@app.route('/create_category', methods=['POST'])
def create_category():
    categoryName = request.form['categoryName']
    categoryDescription = request.form['categoryDescription']
    pic = request.files['file']
    userId = request.form['userId']
    imgId = request.form['imgId']
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            controller = CategoryAPI.CategoryAPI()
            cat = Category.Category(categoryName, categoryDescription, imgId, userId)
            image = CategoryImage.CategoryImage(pic, imgId, userId)
            insert_id = controller.insert(cat, image)
            insert_result = controller.list_user_creation(userId)
        except ValueError as exc:
            error_message = str(exc)
    return render_template(
            'createCategory.html', inserted_data=insert_result, user_data=claims)


@app.route('/create_report', methods=['POST'])
def create_report():
    # Report ID and Image ID need to be unique
    reportId = request.form['reportId']
    userId = request.form['userId']
    placeName = request.form['placeName']
    coordinates = request.form['coordinates']
    categoryId = request.form['categoryId']
    imgId = request.form['imgId']
    review = request.form['review']
    rating = request.form['rating']
    tagId = request.form['tagId']
    pic = request.files['file']
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            repController = ReportAPI.ReportAPI()
            report = Report.Report(reportId, userId, placeName, coordinates, categoryId, imgId, review, rating)
            image = Image.Image(pic, imgId, reportId, userId, tagId)
            insert_id = repController.add_report(report, image)
        except ValueError as exc:
            error_message = str(exc)
    return redirect(url_for('createReport'))


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
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)
            user_controller = UserAPI.UserAPI()
            user = User.User(claims["email"], claims["name"])
            search_user = user_controller.insert(user)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, times=times)


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
