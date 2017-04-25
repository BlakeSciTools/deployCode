from database_manager import DatabaseManager

class Category:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def addToDatabase(self):
        DatabaseManager().addCategory(self)

    def updateInDatabase(self):
        DatabaseManager().updateCategory(self)

    def deleteFromDatabase(self):
        DatabaseManager().deleteCategory(self)

    @staticmethod
    def createCategoryTable():
        DatabaseManager().createCategoryTable()

    @staticmethod
    def getWithId(id):
        dicts = DatabaseManager().getCategoryById(id)
        if (len(dicts) == 1):
            return Category.getObjectFromDictionary(dicts[0])
        else:
            return None

    @staticmethod
    def getAll():
        dicts = DatabaseManager().getCategories()
        categories = []

        for dict in dicts:
            categories.append(Category.getObjectFromDictionary(dict))

        return categories

    @staticmethod
    def getAllAsDicts():
        return DatabaseManager().getCategories()

    @staticmethod
    def getObjectFromDictionary(dict):
        return Category(dict["id"], dict["name"])