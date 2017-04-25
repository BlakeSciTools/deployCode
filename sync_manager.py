from passlib.hash import bcrypt
from http.server import BaseHTTPRequestHandler
from http import cookies
import json

from question import *
from question_log import *
from category import *
from user import *
from session_store import *


class SyncManager(BaseHTTPRequestHandler):

    def getComponentsFromPath(self):
        components = self.path.split('/')
        categories = None
        categorId = None
        questions = None
        questionId = None
        questionLogs = None
        questionLogId = None

        if len(components) >= 2:
            categories = components[1]
        if len(components) >= 3:
            categorId = components[2]
        if len(components) >= 4:
            questions = components[3]
        if len(components) >= 5:
            questionId = components[4]
        if len(components) >= 6:
            questionLogs = components[5]
        if len(components) >= 7:
            questionLogId = components[6]

        return [categories, categorId, questions, questionId, questionLogs, questionLogId]

    def load_session(self):
        sessionStore = SessionStore.getSessionStore()

        if "SessionId" in self.cookie:
            sessionId = self.cookie["SessionId"].value
            self.session = sessionStore.getSession(sessionId)

            if self.session == None:
                newSessionId = sessionStore.createSession("")
                self.session = sessionStore.getSession(newSessionId)

        else:
            newSessionId = sessionStore.createSession("")
            self.cookie["SessionId"] = newSessionId
            self.session = sessionStore.getSession(newSessionId)

        return

    def load_cookie(self):
        if "Cookie" in self.headers:
            self.cookie = cookies.SimpleCookie(self.headers["Cookie"])
        else:
            self.cookie = cookies.SimpleCookie()

    def send_cookie(self):
        for morsel in self.cookie.values():
            self.send_header("Set-Cookie", morsel.OutputString())



    #Responses
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-type")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        self.load_cookie()
        self.load_session()

        if self.session.userId == None or self.session.userId == "":
            self.handle401()
            return

        components = self.getComponentsFromPath()

        if components[0] == "users":
            if components[1] == None:
                self.getUsers()
            else:
                self.getUserWithUsername(components[1])

        elif components[0] == "categories":
            if components[1] == None: #all categories
                self.getCategories()
                return
            elif components[2] == None:
                self.getCategory(components[1])
                return
            elif components[2] == "questions":
                if components[3] == None: #all questions
                    self.getQuestions(components[1])
                    return
                elif components[4] == None:
                    self.getQuestion(components[3])
                    return
                elif components[4] == "question-logs":
                    if components[5] == None: #all question logs
                        self.getQuestionLogs(components[3])
                        return
                    else:
                        self.getQuestionLog(components[5])
                        return

            elif components[2] == "question-logs":
                if components[3] == None:  # all question logs
                    self.getCategoryQuestionLogs(components[1])
                    return
                else:
                    self.getQuestionLog(components[3])
                    return


        self.handle404()

    def do_POST(self):
        components = self.getComponentsFromPath()
        print(components)

        if components[0] == "users":
            if components[1] == None:
                self.createUser()
                return

        self.load_cookie()
        self.load_session()

        if components[0] == "sessions":
            if components[1] == None:
                self.createSession()
                return
        else:
            if self.session.sessionId != None:
                self.handle401()
                return

            if components[0] == "categories":
                if components[1] == None:  # all categories
                    self.createCategory()
                    return
                elif components[2] == "questions":
                    if components[3] == None:  # all questions
                        self.createQuestion()
                        return
                    elif components[4] == "question-logs":
                        if components[5] == None:  # all question logs
                            self.createQuestionLog()
                            return

        self.handle404()

    def do_PUT(self):
        self.load_cookie()
        self.load_session()

        if self.session.userId == None:
            self.handle401()
            return

        components = self.getComponentsFromPath()

        if components[0] == "categories":
            if components[1] != None and components[2] == None:
                self.updateCategory(components[1])
                return
            elif components[2] == "questions":
                if components[3] != None and components[4] == None :
                    self.updateQuestion(components[3])
                    return
                elif components[4] == "question-logs":
                    if components[5] != None:
                        self.updateQuestionLog(components[5])
                        return

        self.handle404()

    def do_DELETE(self):
        self.load_cookie()
        self.load_session()

        if self.session.userId == None:
            self.handle401()
            return

        components = self.getComponentsFromPath()

        if components[0] == "categories":
            if components[1] != None and components[2] == None:
                self.deleteCategory(components[1])
                return
            elif components[2] == "questions":
                if components[3] != None and components[4] == None:
                    self.deleteQuestion(components[3])
                    return
                elif components[4] == "question-logs":
                    if components[5] != None:
                        self.deleteQuestionLog(components[5])
                        return

        self.handle404()


    #Gets
    def getUsers(self):
        objects = User.getAllAsDicts()
        data = json.dumps(objects)
        self.handleGet200(data)

    def getUserWithUsername(self, username):
        object = User.getWithUsername(username)

        if object == None:
            self.handle404()
        else:
            data = json.dumps(object.__dict__)
            self.handleGet200(data)

    def getQuestions(self, categoryId):
        objects = Question.getAllAsDicts(categoryId)
        data = json.dumps(objects)
        self.handleGet200(data)

    def getQuestion(self, questionId):
        object = Question.getWithId(questionId)

        if object == None:
            self.handle404()
        else:
            data = json.dumps(object.__dict__)
            self.handleGet200(data)

    def getCategoryQuestionLogs(self, categoryId):
        questions = Question.getAll(categoryId)
        allQuestionLogs = []
        allQuestionLogDicts = []

        for question in questions:
            questionLogs = QuestionLog.getAll(question.id)

            for log in questionLogs:
                allQuestionLogs.append(log)

        allQuestionLogs.sort()

        for questionLog in allQuestionLogs:
            allQuestionLogDicts.append(questionLog.getAsDict())

        data = json.dumps(allQuestionLogDicts)
        self.handleGet200(data)


    def getQuestionLogs(self, questionId):
        objects = QuestionLog.getAllAsDicts(questionId)
        data = json.dumps(objects)
        self.handleGet200(data)

    def getQuestionLog(self,questionLogId):
        object = QuestionLog.getWithId(questionLogId)

        if object == None:
            self.handle404()
        else:
            data = json.dumps(object.__dict__)
            self.handleGet200(data)

    def getCategories(self):
        objects = Category.getAllAsDicts()
        data = json.dumps(objects)
        self.handleGet200(data)

    def getCategory(self, id):
        object = Category.getWithId(id)

        if object == None:
            self.handle404()
        else:
            data = json.dumps(object.__dict__)
            self.handleGet200(data)

    def handleGet200(self, data):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(data, "utf-8"))


    #Posts
    def createSession(self):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        user = User.getWithUsername(dict["username"])

        if (user != None):
            if bcrypt.verify(dict["password"], user.password):
                self.handle201()
                self.load_cookie()
                self.load_session()
                self.session.userId = user.id
                return

        self.handle401()

    def createQuestion(self):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        Question(1, dict["question"], dict["answer"], dict["false_answer_1"],
                 dict["false_answer_2"], dict["false_answer_3"], dict["category_id"],
                 dict["correct_count"], dict["incorrect_count"]).addToDatabase()
        self.handle201()

    def createQuestionLog(self):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        log = QuestionLog(1, dict["question_id"], dict["correct"],
                    dict["selected_answer"])
        log.addToDatabase()
        self.handle201()

    def createCategory(self):
        length = int(self.headers["content-length"])
        dict = self.rfile.read(length).decode("utf-8")
        Category(1, dict["name"]).addToDatabase()
        self.handle201()

    def createUser(self):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))

        if User.getWithUsername(dict["username"]) == None:
            password = bcrypt.hash(dict["password"])

            user = User(1, dict["username"], password, dict["first_name"], dict["last_name"], dict["email"], dict["permission"])
            user.addToDatabase()

            self.load_cookie()
            self.load_session()
            self.session.userId = user.id
            self.handle201()
        else:
            self.handle422()

    def handle201(self):
        self.send_response(201)
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_cookie()
        self.end_headers()


    #Puts
    def updateQuestion(self, questionId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))

        print(dict["id"])
        if (Question.getWithId(questionId) != None):
            Question(dict["id"], dict["question"], dict["answer"], dict["false_answer_1"],
                     dict["false_answer_2"], dict["false_answer_3"], dict["category_id"],
                     dict["correct_count"], dict["incorrect_count"]).updateInDatabase()
            self.handlePut200()
        else:
            self.handle404()

    def updateQuestionLog(self, questionLogId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))

        if (QuestionLog.getWithId(questionLogId) != None):
            QuestionLog(dict["id"], dict["question_id"], dict["correct"],
                        dict["selected_answer"]).updateInDatabase()
            self.handlePut200()
        else:
            self.handle404()

    def updateCategory(self, categoryId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))

        if (Category.getWithId(categoryId) != None):
            Category(dict["id"], dict["name"]).updateInDatabase()
            self.handlePut200()
        else:
            self.handle404()

    def handlePut200(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()


    # Delete
    def deleteQuestion(self, questionId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        question = Question.getWithId(questionId)

        if (question != None):
            question.deleteFromDatabase()
            self.handlePut200()
        else:
            self.handle404()

    def deleteQuestionLog(self, questionLogId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        questionLog = QuestionLog.getWithId(questionLogId)

        if (questionLog != None):
            questionLog.deleteFromDatabase()
            self.handlePut200()
        else:
            self.handle404()

    def deleteCategory(self, categoryId):
        length = int(self.headers["content-length"])
        dict = json.loads(self.rfile.read(length).decode("utf-8"))
        category = Category.getWithId(categoryId)

        if (category != None):
            category.deleteFromDatabase()
            self.handlePut200()
        else:
            self.handle404()


    #General
    def handle404(self):
        self.send_response(404)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.end_headers()
        self.wfile.write(bytes("<strong>Not Found</strong>", "utf-8"))

    def handle401(self):
        self.send_response(401)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.end_headers()
        self.wfile.write(bytes("<strong>Wrong username or password</strong>", "utf-8"))

    def handle422(self):
        self.send_response(422)
        self.send_header("Content-type", "text/html")
        self.send_header("Access-Control-Allow-Headers", "Content-type")
        self.send_header("Access-Control-Allow-Origin", self.headers["Origin"])
        self.send_header("Access-Control-Allow-Credentials", "true")
        BaseHTTPRequestHandler.end_headers(self)
        self.wfile.write(bytes("<strong>Username taken</strong>", "utf-8"))