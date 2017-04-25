from database_manager import DatabaseManager

class User:
    def __init__(self, id, username, password, firstName, lastName, email, permission):
        self.id = id
        self.username = username
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.permission = permission

    def addToDatabase(self):
        DatabaseManager().addUser(self)

    def updateInDatabase(self):
        DatabaseManager().updateUser(self)

    def deleteFromDatabase(self):
        DatabaseManager().deleteUser(self)

    @staticmethod
    def createUserTable():
        DatabaseManager().createUserTable()

    @staticmethod
    def getWithId(id):
        dicts = DatabaseManager().getUserById(id)
        if (len(dicts) == 1):
            return User.getObjectFromDictionary(dicts[0])
        else:
            return None

    @staticmethod
    def getWithUsername(username):
        dicts = DatabaseManager().getUserByUsername(username)
        if (len(dicts) == 1):
            return User.getObjectFromDictionary(dicts[0])
        else:
            return None

    @staticmethod
    def getAll():
        dicts = DatabaseManager().getUsers()
        users = []

        for dict in dicts:
            users.append(User.getObjectFromDictionary(dict))

        return users

    @staticmethod
    def getAllAsDicts():
        return DatabaseManager().getUsers()

    @staticmethod
    def getObjectFromDictionary(dict):
        return User(dict["id"], dict["username"], dict["password"], dict["first_name"], dict["last_name"], dict["email"], dict["permission"])
