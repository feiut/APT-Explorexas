
from userCollectionAPI import UserCollectionAPI
from User import User

def testUserAPI():

    # 1. Create User
    controller = UserCollectionAPI()
    print('--- Insert a user into the Users collection ---')
    user = User("linsong", "19961106", "song@utexas.edu", "male", "11-1996")
    inserted_id = controller.insert(user)
    assert(inserted_id is not None)
    print("Insert Test Passed")

    # 2. Delete User
    print('--- Delete a user from the Users collection ---')
    result = controller.delete('_id', inserted_id)
    assert(result.deleted_count == 1)
    print("Delete Test1 using id Passed")

    user = User("linsong", "19961106", "song@utexas.edu", "male", "11-1996")
    inserted_id = controller.insert(user)
    result = controller.delete('username', user.username)
    assert (result.deleted_count == 1)
    print("Delete Test2 using username Passed")

    user = User("linsong", "19961106", "song@utexas.edu", "male", "11-1996")
    inserted_id = controller.insert(user)
    result = controller.delete('email', user.email)
    assert (result.deleted_count == 1)
    print("Delete Test3 using email Passed")

    # 3. List Users
    print('--- List Users from the Users collection ---')
    user2 = User("qinsong", "19971106", "wang@utexas.edu", "female", "10-1996")
    inserted_id2 = controller.insert(user2)
    users = controller.list()
    print users
    print("list returns ", len(users), " rows.")
    assert(len(users) >= 3)
    print("List Test Passed")

    # 4. Get Users
    print('--- Get User from the Users collection ---')
    retrieved = controller.get('_id', inserted_id2)
    assert(retrieved.username == user2.username)
    print("Get Test1 using id Passed")

    retrieved = controller.get('username', user2.username)
    assert (retrieved.username == user2.username)
    print("Get Test2 using username Passed")

    # 5. Update Users
    print('--- Update User from the Users collection ---')
    retrieved.email = "linfeng@utexas.edu"
    controller.update(retrieved)
    updated = controller.get('_id', inserted_id2)
    assert(updated.email == "linfeng@utexas.edu")
    print("Update Test Passed")

if __name__ == '__main__':
    testUserAPI()




