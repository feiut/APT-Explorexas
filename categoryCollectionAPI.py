from commonAPI import *

#[input]  name
#[return] _id of inserted category
def insert_category(name):
    cat = connect_to_database('Categories')
    query = {'Name':name}
    srchRlt = cat.find_one(query)
    if srchRlt is None:
        rlt = cat.insert_one(query)
        print('The category:{name} created successfully & the id is {id}'.format(name = name, id =str(rlt.inserted_id)))
        return rlt.inserted_id
    else:
        print('The category already exists, id is:'+ str(srchRlt['_id']))
        return srchRlt['_id']

#[input]  field & corresponding value
#[return] None
def delete_category(field, val):
    cat = connect_to_database('Categories')
    query = {field:val}
    srchRlt = cat.find_one(query)
    if srchRlt is None:
        print('The category does not exist')
    else:
        name = srchRlt['Name']
        delRlt = cat.delete_one(query)
        print('there is {num} category deleted successfully, Name:{name}'.format(num = delRlt.deleted_count, name = name))

#[input]  field & corresponding value
#[return] retireved category (class:dict)
def retrieve_category(field, val):
    cat = connect_to_database('Categories')
    query = {field:val}
    srchRlt = cat.find_one(query)
    if srchRlt is None:
        print('The category does not exist')
    else:
        print(srchRlt)
        return srchRlt

#[input]  None
#[return] retireved all category (class:cursor)
def retrieve_all_category():
    cat = connect_to_database('Categories')
    srchRlt = cat.find()
    for doc in srchRlt:
        print(doc)
    return cat.find()

#[input]  oldName & newName
#[return] _id of updated category
def update_category(oldName, newName):
    cat = connect_to_database('Categories')
    oldSrchRlt = cat.find_one({'Name':oldName})
    newSrchRlt = cat.find_one({'Name':newName})
    if newSrchRlt is None:
        if oldSrchRlt is None:
            insert_category(newName)
        else:
            cat.update_one({'Name':oldName}, {'$set':{'Name':newName}})
            print('The updated new category name is:'+ newName)
            return cat.find_one({'Name':newName})['_id']
    else:
        print('The new name already exist')
        return newSrchRlt['_id']