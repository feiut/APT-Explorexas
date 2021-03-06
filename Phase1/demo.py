from UserAPITest import testUserAPI
from PlaceAPITest import testPlaceAPI
from CategoryTagAPITest import testCatAPI, testTagAPI
from Report_ImgAPITest import testReportAPI, testImageAPI


if __name__ == '__main__':
    print("Test User API: ")
    testUserAPI()

    print("Test Place API: ")
    testPlaceAPI()

    print("Test Category API: ")
    testCatAPI()

    print("Test Tag API: ")
    testTagAPI()

    print("Test Report API: ")
    testReportAPI()

    print("Test Image API: ")
    testImageAPI()

    print("All Test Passed!")
