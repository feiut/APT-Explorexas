import pymongo
from userCollectionAPI import *
from categoryCollectionAPI import *
from tagCollectionAPI import *


print('***************************************************')
print('******************** USER API *********************')
print('***************************************************')

# 1. Insert_user
# 2. Delete_user
# 3. Update_user
# 4. Retrieve_user
# 5. Retrieve_user_by_filed
# 6. Get_user_info
# 7. Valid_password (Used in log-in)
# 8. Is_admin_or_not

# 1. Create User
#print('Enter the user information you want to create: ')
# username = raw_input('Username: ')
# password = raw_input('Password: ')
# email = raw_input('Email: ')
# gender = raw_input('Gender: ')
# dateOfBirth = raw_input('Date of Birth (mm-yyyy): ')
print('--- Insert a user into the Users collection ---')
username = 'wasong'
password = '19961106'
email = 'song@utexas.edu'
gender = 'male'
dateOfBirth = '11-1996'
insert_user(username, password, email, gender, dateOfBirth)

# 2. Delete User
print('')
print('--- Delete a user from the Users collection ---')
print('Enter the username you want to delete: ')
username = raw_input('Username: ')
delete_user(username)

# 3. Update User
print('')
print('--- Update user info in the Users collection ---')
#print('Enter the user information you want to update: ')
# username = raw_input('Username: ')
# password = raw_input('Password: ')
# email = raw_input('Email: ')
# gender = raw_input('Gender: ')
# dateOfBirth = raw_input('Date of Birth (mm-yyyy): ')
username = 'wangsong'

print('--- Before updating, the user info is: ---')
retrieve_user_by_field('username', username)

print('*** Update password of wangsong ***')
password = '19961106'
update_user_password(username, password)

print('*** Update email of wangsong ***')
email = 'song123@utexas.edu'
update_user_email(username, email)

print('*** Update gender of wangsong ***')
gender = 'female'
update_user_gender(username, gender)

print('*** Update dateOfBirth of wangsong ***')
dateOfBirth = '10-1996'
update_user_dateOfBirth(username, dateOfBirth)

print('*** Update dateOfRegistration of wangsong ***')
dateOfRegistration = '08-2019'
update_user_dateOfRegistration(username, dateOfRegistration)

print('*** Update role of wangsong ***')
role = 'visitor'
update_user_role(username, role)

print('*** Update all fields of wangsong ***')
update_user(username, password, email, gender, dateOfBirth, dateOfRegistration, role)

print('--- After updating, the user info is: ---')
retrieve_user_by_field('username', username)

# 4. Retrieve User
print('')
print('--- Retrieve all users information: ---')
dict = retrieve_user()

# 5. Retrieve User According to one field
print('')
print('--- Retrieve users information using specific fields ---')
print('--- Here we list all female users: ---')
field = 'gender'
retrieve = 'female'
dict = retrieve_user_by_field(field, retrieve)

# 6. Retrieve A Specific Info of A User
print('')
print('--- Retrieve a specific info of a user: ---')
field = 'email'
username = 'wangsong'
result = get_user_email(username)
print 'The ' + field + ' of ' + username + ' is : ' + result

field = 'gender'
result = get_user_gender(username)
print 'The ' + field + ' of ' + username + ' is : ' + result

field = 'dateOfBirth'
result = get_user_dateOfBirth(username)
print 'The ' + field + ' of ' + username + ' is : ' + result

field = 'dateOfRegistration'
result = get_user_dateOfRegistration(username)
print 'The ' + field + ' of ' + username + ' is : ' + result

field = 'role'
result = get_user_role(username)
print 'The ' + field + ' of ' + username + ' is : ' + result

# 7. Get password of the user and validate the password
print('')
print('--- Validate the password of a user: ---')
username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')
validOrNot = validate_password(username, password)

# 8. Check whether this user is admin
print('')
print('--- Check the role of a user: ---')
username = 'wangsong'
result = is_admin_or_not(username)
print('User ' + username + ' is admin or not? ' + str(result))

print('***************************************************')
print('****************** CATEGORY API *******************')
print('***************************************************')

# 1. clear all documents for initialization
# 2. insert a category
# 3. retrieve a category
# 4. update a category
# 5. insert another category
# 6. retrieve a category by id
# 7. list all categories
# 8. delete a category
# 9. list all categories
# 10. demo end

# 1. clear all documents for initialization
col = connect_to_database('Categories')
col.delete_many({})
print('categories collection APIs demo starts!!!')
# 2. insert a category
print('------------------')
print('insert the new category: Hiking')
name = 'Hiking'
insert_category(name)
# 3. retrieve a category by name
print('------------------')
print('retrieve the category you just inserted by name')
retrieve_category('Name', name)
# 4. update a category
print('------------------')
print('update the category "Hiking" to "Swimming"')
newName = 'Swimming'
id = update_category(name, newName)
retrieve_category('_id', id)
# 5. insert another category
print('------------------')
print('insert the another new category: Diving')
name = 'Diving'
id = insert_category(name)
# 6. retrieve a category by id
print('------------------')
print('retrieve the category you just inserted by ID')
retrieve_category('_id', id)
# 7. retrieve all categorys
print('------------------')
print('retrieve all categories')
retrieve_all_category()
# 8. delete a category
print('------------------')
print('delete the category "Swimming"')
name = 'Swimming'
delete_category('Name',name)
# 9. retrieve all categorys
print('------------------')
print('retrieve all categories')
retrieve_all_category()
#10 demo end
print('------------------')

print('***************************************************')
print('********************* TAG API *********************')
print('***************************************************')

# 1. clear all documents for initialization
# 2. insert a tag
# 3. retrieve a tag
# 4. update a tag
# 5. insert another tag
# 6. retrieve a tag by id
# 7. list all tags
# 8. delete a tag
# 9. list all tags
# 10. demo end

# 1. clear all documents for initialization
col = connect_to_database('Tags')
col.delete_many({})
print('tags collection APIs demo starts!!!')
# 2. insert a tag
print('------------------')
print('insert the new tag: HappyLife')
name = 'HappyLife'
insert_tag(name)
# 3. retrieve a tag by name
print('------------------')
print('retrieve the tag you just added by name')
retrieve_tag('Name', name)
# 4. update a tag
print('------------------')
print('update the tag name from "HappyLife" to "HappyHour"')
newName = 'HappyHour'
id = update_tag(name, newName)
retrieve_tag('_id', id)
# 5. insert another tag
print('------------------')
print('insert the new tag: Wonderful Land')
name = 'Wonderful Land'
id = insert_tag(name)
# 6. retrieve a tag by id
print('------------------')
print('retrieve the tag you just added by ID')
retrieve_tag('_id', id)
# 7. retrieve all tags
print('------------------')
print('retrieve all tags')
retrieve_all_tag()
# 8. delete a tag
print('------------------')
print('delete the tag: HappyHour')
name = 'HappyHour'
delete_tag('Name',name)
# 9. retrieve all tags
print('------------------')
print('retrieve all tags')
retrieve_all_tag()
#10 demo end
print('------------------')