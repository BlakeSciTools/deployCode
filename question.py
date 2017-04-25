from database_manager import DatabaseManager

class Question:
    def __init__(self, id, question, answer, falseAnswer1, falseAnswer2, falseAnswer3, categoryId, correctCount, incorrectCount):
        self.id = id
        self.question = question
        self.answer = answer
        self.falseAnswer1 = falseAnswer1
        self.falseAnswer2 = falseAnswer2
        self.falseAnswer3 = falseAnswer3
        self.categoryId = categoryId
        self.correctCount = correctCount
        self.incorrectCount = incorrectCount

    def addToDatabase(self):
        DatabaseManager().addQuestion(self)

    def updateInDatabase(self):
        DatabaseManager().updateQuestion(self)

    def deleteFromDatabase(self):
        DatabaseManager().deleteQuestion(self)

    @staticmethod
    def createQuestionTable():
        DatabaseManager().createQuestionTable()

    @staticmethod
    def getWithId(id):
        dicts = DatabaseManager().getQuestionById(id)
        if (len(dicts) == 1):
            return Question.getObjectFromDictionary(dicts[0])
        else:
            return None

    @staticmethod
    def getAll(categoryId):
        dicts = DatabaseManager().getQuestions(categoryId)
        questions = []

        for dict in dicts:
            questions.append(Question.getObjectFromDictionary(dict))

        return questions

    @staticmethod
    def getAllAsDicts(categoryId):
        return DatabaseManager().getQuestions(categoryId)

    @staticmethod
    def getObjectFromDictionary(dict):
        return Question(dict["id"], dict["question"], dict["answer"], dict["false_answer_1"], dict["false_answer_2"], dict["false_answer_3"], dict["category_id"], dict["correct_count"], dict["incorrect_count"])
