import json
import os
import psycopg2
import psycopg2.extras
import urllib.parse

class DatabaseManager:
    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()
        return

    def __del__(self):
        self.connection.close()
        return


    # CREATE TABLES
    def createUserTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255), username VARCHAR(255), password VARCHAR(255), permission INTEGER)")

    def createQuestionTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS question (id SERIAL PRIMARY KEY, question VARCHAR(255), answer VARCHAR(255), false_answer_1 VARCHAR(255), false_answer_2 VARCHAR(255), false_answer_3 VARCHAR(255), category_id INTEGER, correct_count INTEGER, incorrect_count INTEGER)")

    def createQuestionLogTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS questionLog (id SERIAL PRIMARY KEY, question_id INTEGER, correct INTEGER, selected_answer VARCHAR(255))")

    def createCategoryTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS category (id SERIAL PRIMARY KEY, name VARCHAR(255))")


    # QUESTIONS
    def getQuestions(self, categoryId):
        self.cursor.execute("SELECT * FROM question WHERE category_id == %s", (categoryId,))
        return self.cursor.fetchall()

    def getQuestionById(self, id):
        self.cursor.execute("SELECT * FROM question WHERE id = %s", (id,))
        return self.cursor.fetchall()

    def addQuestion(self, question):
        self.cursor.execute("INSERT INTO question (question, answer, false_answer_1, false_answer_2, false_answer_3, category_id, correct_count, incorrect_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (question.question, question.answer, question.falseAnswer1, question.falseAnswer2, question.falseAnswer3, question.categoryId, question.correctCount, question.incorrectCount))
        self.connection.commit()
        return

    def updateQuestion(self, question):
        self.cursor.execute("UPDATE question SET question = %s, answer = %s, false_answer_1 = %s, false_answer_2 = %s, false_answer_3 = %s, category_id = %s, correct_count = %s, incorrect_count = %s WHERE id = %s", (question.question, question.answer, question.falseAnswer1, question.falseAnswer2, question.falseAnswer3, question.categoryId, question.correctCount, question.incorrectCount, question.id))
        self.connection.commit()

    def deleteQuestion(self, question):
        self.cursor.execute("DELETE FROM question WHERE id = %s", (question.id,))
        self.connection.commit()


    #QUESTION LOGS
    def getQuestionLogs(self, questionId):
        self.cursor.execute("SELECT * FROM questionLog WHERE question_id = %s", (questionId,))
        return self.cursor.fetchall()

    def getQuestionLogById(self, id):
        self.cursor.execute("SELECT * FROM questionLog WHERE id = %s", (id,))
        return self.cursor.fetchall()

    def addQuestionLog(self, questionLog):
        self.cursor.execute("INSERT INTO questionLog (question_id, correct, selected_answer) VALUES (%s, %s, %s)", (questionLog.questionId, questionLog.correct, questionLog.selectedAnswer))
        self.connection.commit()
        return

    def updateQuestionLog(self, questionLog):
        self.cursor.execute("UPDATE questionLog SET question_id = %s, correct = %s, selected_answer = %s WHERE id = %s", (questionLog.questionId, questionLog.correct, questionLog.selectedAnswer, questionLog.id))
        self.connection.commit()

    def deleteQuestionLog(self, questionLog):
        self.cursor.execute("DELETE FROM questionLog WHERE id = %s", (questionLog.id,))
        self.connection.commit()


    #CATEGORIES
    def getCategories(self):
        self.cursor.execute("SELECT * FROM category")
        return self.cursor.fetchall()

    def getCategoryById(self, id):
        self.cursor.execute("SELECT * FROM category WHERE id = %s", (id,))
        return self.cursor.fetchall()

    def addCategory(self, category):
        self.cursor.execute("INSERT INTO category (name) VALUES (%s)", (category.name,))
        self.connection.commit()
        return

    def updateCategory(self, category):
        self.cursor.execute("UPDATE category SET name = %s WHERE id = %s", (category.name, category.id))
        self.connection.commit()

    def deleteCategory(self, category):
        self.cursor.execute("DELETE FROM category WHERE id = %s", (category.id,))
        self.connection.commit()


    #USERS
    def getUsers(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def getUserById(self, id):
        self.cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        return self.cursor.fetchall()

    def getUserByUsername(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return self.cursor.fetchall()

    def addUser(self, user):
        self.cursor.execute("INSERT INTO users (username, password, first_name, last_name, email, permission) VALUES (%s, %s, %s, %s, %s, %s)", (user.username, user.password, user.firstName, user.lastName, user.email, user.permission))
        self.connection.commit()
        return

    def updateUser(self, user):
        self.cursor.execute("UPDATE users SET username = %s, password = %s, first_name = %s, last_name = %s, email = %s, permission = %s WHERE id = %s", (user.username, user.password, user.firstName, user.lastName, user.email, user.permission, user.id))
        self.connection.commit()

    def deleteUser(self, user):
        self.cursor.execute("DELETE FROM users WHERE id = %s", (user.id,))
        self.connection.commit()