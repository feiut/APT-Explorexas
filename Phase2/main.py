from flask import Flask, render_template, request, redirect, url_for
from google.auth.transport import requests
from google.cloud import datastore
import google.oauth2.id_token
from lib import Category, CategoryAPI

app = Flask(__name__)
datastore_client = datastore.Client()
firebase_request_adapter = requests.Request()

# Enter the createCategory page
@app.route('/createCategory')
def createCategory():
    return render_template('createCategory.html')


# Insert a new category to the database
@app.route('/create_category', methods=['POST'])
def create_category():
    categoryName = request.form['categoryName']
    categoryDescription = request.form['categoryDescription']
    pic = request.files['file']
    id_token = request.cookies.get("token")
    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(id_token, firebase_request_adapter)
            controller = CategoryAPI.CategoryAPI()
            cat = Category.Category(categoryName, categoryDescription, pic)
            insert_id = controller.insert(cat)
        except ValueError as exc:
            error_message = str(exc)
    return redirect(url_for('createCategory'))


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
    app.run(host='127.0.0.1', port=8080, debug=True)
    # db = get_db_collection()
