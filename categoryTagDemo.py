from categoryAPI import CategoryAPI
from tagCollectionAPI import TagAPI
from Category import Category
from Tag import Tag

def testTagAPI():
    controller = TagAPI()
    print("Test insertion")
    tag = Tag("dummy name")
    inserted_id = controller.insert(tag)
    assert(inserted_id is not None)
    print("Passed")

    print("Test list")
    tag2 = Tag("another dummy name")
    inserted_id2 = controller.insert(tag2)
    tags = controller.list()
    print("list returns ", len(tags), " rows.")
    assert(len(tags) >= 2)
    print("Passed")

    print("Test retrieval")
    retrieved = controller.get(inserted_id)
    assert(retrieved.tagName == tag.tagName)
    print("Passed")

    print("Test update")
    retrieved.tagName = "change name"
    controller.update(retrieved)
    updated = controller.get(inserted_id)
    assert(updated.tagName == "change name")
    print("Passed")

    print("Test deletion")
    result = controller.delete(inserted_id)
    assert(result.deleted_count == 1)
    controller.delete(inserted_id2)
    print("Passed")


def testCatAPI():
    controller = CategoryAPI()
    print("Test insertion")
    cat = Category("dummy name")
    inserted_id = controller.insert(cat)
    assert(inserted_id is not None)
    print("Passed")

    print("Test list")
    cat2 = Category("another dummy name")
    inserted_id2 = controller.insert(cat2)
    cats = controller.list()
    print("list returns ", len(cats), " rows.")
    assert(len(cats) >= 2)
    print("Passed")

    print("Test retrieval")
    retrieved = controller.get(inserted_id)
    assert(retrieved.catName == cat.catName)
    print("Passed")

    print("Test update")
    retrieved.catName = "change name"
    controller.update(retrieved)
    updated = controller.get(inserted_id)
    assert(updated.catName == "change name")
    print("Passed")

    print("Test deletion")
    result = controller.delete(inserted_id)
    assert(result.deleted_count == 1)
    controller.delete(inserted_id2)
    print("Passed")


if __name__ == '__main__':
    testTagAPI()
    testCatAPI()