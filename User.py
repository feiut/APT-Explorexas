import datetime

class User:
    def __init__(self, username, password, email, gender, dateOfBirth, dateOfRegistration = None, role = "user", user_id = None):
        self.username = username
        self.password = password
        self.email = email
        self.gender = gender
        self.dateOfBirth = dateOfBirth
        self.dateOfRegistration = compute_date_of_registration(self)
        self.role = role
        self.user_id = user_id


    def toQuery(self):
        query = { "username": self.username, "password": self.password, "email": self.email, "gender": self.gender, "dateOfBirth": self.dateOfBirth, "dateOfRegistration": self.dateOfRegistration, "role": self.role}
        return query


def compute_date_of_registration(self):
    # Compute date of registration
    if datetime.datetime.now().month < 10:
        dateMonth = '0' + str(datetime.datetime.now().month)
    else:
        dateMonth = datetime.datetime.now().month
    dateYear = datetime.datetime.now().year
    return str(dateMonth) + '-' + str(dateYear)
