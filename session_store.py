import base64, os

class SessionStore:

    sessionStore = None

    @staticmethod
    def getSessionStore():
        if SessionStore.sessionStore == None:
            SessionStore.sessionStore = SessionStore()

        return SessionStore.sessionStore

    def __init__(self):
        self.sessions = {}

    def createSession(self, userId):
        for session in self.sessions.values():
            if session.userId == userId:
                return session.sessionId

        newSession = Session(userId)
        self.sessions[newSession.sessionId] = newSession

        return newSession.sessionId

    def getSession(self, sessionId):
        if sessionId in self.sessions.keys():
            return self.sessions[sessionId]

        return None


class Session:
    def __init__(self, userId):
        randNum = os.urandom(32)

        self.sessionId = base64.b64encode(randNum).decode("utf-8")
        self.userId = userId