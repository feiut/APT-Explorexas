from commonAPI import *

#[input]  name
#[return] _id of inserted tag
def insert_tag(name):
    tag = connect_to_database('Tags')
    query = {'Name':name}
    srchRlt = tag.find_one(query)
    if srchRlt is None:
        rlt = tag.insert_one(query)
        print('The tag:{name} created successfully & the id is {id}'.format(name = name, id =str(rlt.inserted_id)))
        return rlt.inserted_id
    else:
        print('The tag already exists, id is:'+ str(srchRlt['_id']))
        return srchRlt['_id']

#[input]  field & corresponding value
#[return] None
def delete_tag(field, val):
    tag = connect_to_database('Tags')
    query = {field:val}
    srchRlt = tag.find_one(query)
    if srchRlt is None:
        print('The tag does not exist')
    else:
        name = srchRlt['Name']
        delRlt = tag.delete_one(query)
        print('there is {num} tag deleted successfully, Name:{name}'.format(num = delRlt.deleted_count, name = name))

#[input]  field & corresponding value
#[return] retireved tag (class:dict)
def retrieve_tag(field, val):
    tag = connect_to_database('Tags')
    query = {field:val}
    srchRlt = tag.find_one(query)
    if srchRlt is None:
        print('The tag does not exist')
        return None
    else:
        print(srchRlt)
        return srchRlt

#[input]  None
#[return] retireved all tag (class:cursor)
def retrieve_all_tag():
    tag = connect_to_database('Tags')
    srchRlt = tag.find()
    for doc in srchRlt:
        print(doc)
    return tag.find()

#[input]  oldName & newName
#[return] _id of updated tag
def update_tag(oldName, newName):
    tag = connect_to_database('Tags')
    oldSrchRlt = tag.find_one({'Name':oldName})
    newSrchRlt = tag.find_one({'Name':newName})
    if newSrchRlt is None:
        if oldSrchRlt is None:
            insert_tag(newName)
        else:
            tag.update_one({'Name':oldName}, {'$set':{'Name':newName}})
            print('The updated new tag name is:'+newName)
            return tag.find_one({'Name':newName})['_id']
    else:
        print('The new name already exist')
        return newSrchRlt['_id']