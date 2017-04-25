from http.server import HTTPServer
from sync_manager import SyncManager
import sys

from question import *
from question_log import *
from category import *
from user import *

def main():
    port = 8080

    Question.createQuestionTable()
    User.createUserTable()
    Category.createCategoryTable()
    QuestionLog.createQuestionLogTable()


    if len(sys.argv) > 1:
        port = int(sys.argv[1])

    listen = ("0.0.0.0", port)
    server = HTTPServer(listen, SyncManager)
    print("listening")
    server.serve_forever()

    # listen = ("127.0.0.1", 8080)
    # server = HTTPServer(listen, SyncManager)
    # print("listening")
    # server.serve_forever()

main()