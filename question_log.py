from database_manager import DatabaseManager

# CREATE TABLE questionLog (
# id INTEGER PRIMARY KEY,
# question_id INTEGER,
# correct INTEGER,
# selected_answer VARCHAR(255));

class QuestionLog:
    def __init__(self, id, questionId, correct, selectedAnswer):
        self.id = id
        self.questionId = questionId
        self.correct = correct
        self.selectedAnswer = selectedAnswer

    def __eq__(self, other):
        if (other != None and other != False):
            if self.id == other.id:
                return True
        return False

    def __lt__(self, other):
        if self.id < other.id:
            return True
        return False

    def __gt__(self, other):
        if self.id > other.id:
            return True
        return False

    def getAsDict(self):
        return {"id" : self.id, "question_id" : self.questionId,
                "correct" : self.correct}

    def addToDatabase(self):
        DatabaseManager().addQuestionLog(self)

    def updateInDatabase(self):
        DatabaseManager().updateQuestionLog(self)

    def deleteFromDatabase(self):
        DatabaseManager().deleteQuestionLog(self)

    @staticmethod
    def createQuestionLogTable():
        DatabaseManager().createQuestionLogTable()

    @staticmethod
    def getWithId(id):
        dicts = DatabaseManager().getQuestionLogById(id)
        if (len(dicts) == 1):
            return QuestionLog.getObjectFromDictionary(dicts[0])
        else:
            return None

    @staticmethod
    def getAll(questionId):
        dicts = DatabaseManager().getQuestionLogs(questionId)
        questionLogs = []

        for dict in dicts:
            questionLogs.append(QuestionLog.getObjectFromDictionary(dict))

        return questionLogs

    @staticmethod
    def getAllAsDicts(questionId):
        return DatabaseManager().getQuestionLogs(questionId)

    @staticmethod
    def getObjectFromDictionary(dict):
        return QuestionLog(dict["id"], dict["question_id"], dict["correct"], dict["selected_answer"])