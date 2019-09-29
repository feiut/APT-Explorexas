
from commonAPI import connect_to_database

'''

API for Collection - User

0. Connect_to_database
1. Insert_user
2. Delete_user
3. Update_user
    update_user
    update_user_password
    update_user_email
    update_user_gender
    update_user_dateOfBirth
    update_user_dateOfRegistration
    update_user_role
4. Retrieve_user
5. Retrieve_user_by_filed
6. Get_user_info
    get_user_password
    get_user_email
    get_user_gender
    get_user_dateOfBirth
    get_user_dateOfRegistration
    get_user_role
7. Valid_password (Used in log-in)
8. Is_admin_or_not


'''

#[input] username, password, email, gender, dateOfBirth
#[output] _id of inserted user 
def insert_user(username, password, email, gender, dateOfBirth):
    import datetime
    users = connect_to_database("Users")

    # Compute date of registration
    if datetime.datetime.now().month < 10:
        dateMonth = '0' + str(datetime.datetime.now().month)
    else:
        dateMonth = datetime.datetime.now().month

    dateYear = datetime.datetime.now().year
    dateOfRegistration =  str(dateMonth) + '-' + str(dateYear)

    # Check whether the username has already existed
    query = {'username': username}
    searchResult = users.find_one(query)
    if searchResult is None:
        # If not existed, then create this user
        query = {'username': username, 'password': password, 'email': email, 'gender': gender, 'dateOfBirth': dateOfBirth, \
                'dateOfRegistration': dateOfRegistration, 'role': 'user'}
        result = users.insert_one(query)
        # result= users.update_one(query, {'$set': query}, upsert=True)
        print 'The user:{name} created successfully & the id is {id}'.format(name = username, id =str(result.inserted_id))
        return result.inserted_id
    else:
        # If existed, then prompt error
        print('The user already exists, id is:' + str(searchResult['_id']))
        return searchResult['_id']


#[input] username
#[output]  None
def delete_user(username):
    users = connect_to_database("Users")
    # Delete a user according to username
    query = {'username':username}
    if(users.find_one(query) is not None):
        # If the username exists, then delete it
        users.remove(query, {'$delete': query})
        print 'User ' + username + ' deleted successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, password, email, gender, dateOfBirth, dateOfRegistration, role
#[output]  None
def update_user(username, password, email, gender, dateOfBirth, dateOfRegistration, role):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'username': username, 'password': password, 'email': email, 'gender': gender, 'dateOfBirth': dateOfBirth, 'dateOfRegistration': dateOfRegistration, 'role' : role}})
        print 'User ' + username + ' updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, password
#[output]  None
def update_user_password(username, password):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'password': password}})
        print 'User ' + username + ' password updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, email
#[output]  None
def update_user_email(username, email):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'email': email}})
        print 'User ' + username + ' email updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, gender
#[output]  None
def update_user_gender(username, gender):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'gender': gender}})
        print 'User ' + username + ' gender updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, dateOfBirth
#[output]  None
def update_user_dateOfBirth(username, dateOfBirth):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'dateOfBirth': dateOfBirth}})
        print 'User ' + username + ' dateOfBirth updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, dateOfRegistration
#[output]  None
def update_user_dateOfRegistration(username, dateOfRegistration):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'dateOfRegistration': dateOfRegistration}})
        print 'User ' + username + ' dateOfRegistration updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] username, role
#[output]  None
def update_user_role(username, role):
    users = connect_to_database("Users")
    query = {'username': username}
    # Update a user's info according to username
    if(users.find_one(query) is not None):
        # If the user exists, update
        users.update_one({},{'$set':{'role': role}})
        print 'User ' + username + ' role updated successfully.'
    else:
        print 'User ' + username + ' not existed.'


#[input] None
#[output]  Retrieva all users
def retrieve_user():
    users = connect_to_database("Users")
    dict = users.find()
    # Retrieve all users' information
    print 'All users in the dateabase are: '
    for doc in dict:
        print doc
    return dict
    print ''


#[input] field, retrieve
#[output]  Retrieva all users satisfying the field:retrieve
def retrieve_user_by_field(field, retrieve):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {field: retrieve}
    dict = users.find(query)
    if dict is None:
        print 'No match.'
    else:
        for doc in dict:
            print doc
    return dict


#[input] username
#[output]  password
def get_user_password(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['password']


#[input] username
#[output]  email
def get_user_email(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['email']


#[input] username
#[output]  gender
def get_user_gender(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['gender']


#[input] username
#[output]  dateOfBirth
def get_user_dateOfBirth(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['dateOfBirth']


#[input] username
#[output]  dateOfRegistration
def get_user_dateOfRegistration(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['dateOfRegistration']


#[input] username
#[output]  role
def get_user_role(username):
    users = connect_to_database("Users")
    # Retrieve the user information based on given value of given fields
    query = {'username': username}
    dict = users.find_one(query)
    return dict['role']


#[input] username, password
#[output]  True or False
def validate_password(username, password):
    users = connect_to_database("Users")
    query = {'username':username}
    if(users.find_one(query) is not None):
        dict = users.find_one(query)
        if(dict['password']==password):
            return True
        else:
            print 'Incorrect Password.'
            return False
    else:
        print 'User ' +username +' not existed.'
        return False


#[input] username
#[output]  True or False
def is_admin_or_not(username):
    users = connect_to_database("Users")
    query = {'username': username}
    dict = users.find_one(query)
    if(dict['role']=='admin'):
        return True
    else:
        return False

