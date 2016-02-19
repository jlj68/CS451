import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from user import User
import pychess
import random

# {id: (game, whitePlayerWebsocket, blackPlayerWebsocket)}
gamesList = {}

activeUsers = {}
availableUsers = {}
websocketClients = {}
pendingInvites = []

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        if self.get_secure_cookie('username'):
            return None
        return self.get_secure_cookie('username')

class MainHandler(BaseHandler):
    def get(self):
        #if self.current_user is not None:
            self.render("./public/index.html")
        #else:
            #self.write("User not logged in.")

class GameHandler(tornado.web.RequestHandler):
    def put(self):
        gameID = random.randint(1, 1024)
        while gameID in gamesList.keys():
            gameID = random.randint(1, 1024)
        newGame = pychess.Game()
        gamesList[gameID] = newGame
        self.set_secure_cookie('current_game', str(gameID))
        self.write(tornado.escape.json_encode({'gameID': str(gameID) }))

class GamePageHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.render("./public/game.html", gameID=id)

# this will be a web socket class
class GameDataHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(tornado.escape.json_encode({'board': gamesList[int(id)].board.getBoardJson()}))

class MoveHandler(tornado.web.RequestHandler):
    def get(self, id):
        if id == self.get_secure_cookie('current_game'):
            # get moves from a position
            row = int(self.get_argument('row'))
            col = int(self.get_argument('col'))
            moves = gamesList[int(id)].board.getMovesFromPosition(row, col)
            movesList = [{'fromPos': move.fromPos.__dict__, 'toPos': move.toPos.__dict__} for move in moves]
            self.write(tornado.escape.json_encode({ 'moves': movesList }))

    def put(self, id):
        originPosition = pychess.Position(int(self.get_body_argument('fromPosRow')), int(self.get_body_argument('fromPosCol')))
        destPosition = pychess.Position(int(self.get_body_argument('toPosRow')), int(self.get_body_argument('toPosCol')))
        newMove = pychess.Move(originPosition, destPosition)

        if gamesList[int(id)].board.isValidMove(newMove):
            gamesList[int(id)].board.applyMove(pychess.Move(originPosition, destPosition))
            raise tornado.web.HTTPError(200)
        else:
            raise tornado.web.HTTPError(403)

class UserHandler(tornado.web.RequestHandler):
    def get(self):
        userList = []
        for user in availableUsers.keys():
            userList.append(availableUsers[user].__dict__)
        userList = sorted(userList, key = lambda user: user['username'])
        self.write(tornado.escape.json_encode({'users': userList}))

    def put(self):
        username = self.get_body_argument("username")
        if username not in activeUsers.keys() and username not in availableUsers.keys():
            newUser = User(username)
            activeUsers[username] = newUser
            availableUsers[username] = newUser
            self.set_secure_cookie('username', username)
            raise tornado.web.HTTPError(201)
        else:
            raise tornado.web.HTTPError(409)

    def post(self):
        self.write("modifying user")

class UserDataHandler(tornado.web.RequestHandler):
    def get(self, username):
        self.write(tornado.escape.json_encode({'user_data': activeUsers[username].__dict__}))

class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('./public/test.html')

    def post(self):
        self.write(tornado.escape.json_encode({ 'clients': [name.decode('ascii') for name in list(websocketClients.keys())] }))

class InviteSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        websocketClients[self.get_secure_cookie('username').decode('ascii')] = self

    def on_message(self, message):
        messageDict = tornado.escape.json_decode(message)
        if messageDict['function'] == "send":
            pendingInvites.append([websocketClients[messageDict['target']]])
            websocketClients[messageDict['target']].write_message(tornado.escape.json_encode({'request': 'invite'}))
        elif messageDict['function'] == "receive":
            websocketClients[messageDict['sender'].decode('ascii')].write_message(tornado.escape.json_encode({'request': 'invited'}))
        elif messageDict['function'] == "accept":
            print('accepted')
        elif messageDict['function'] == "decline":
            print('declined')

    def on_close(self):
        del websocketClients[self.get_secure_cookie('username').decode('ascii')]
        print("Socket closed")

def make_app():
    return tornado.web.Application([
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': './public/'}),
        (r"/", MainHandler),
        (r"/invite", InviteSocketHandler),
        (r"/users", UserHandler),
        (r"/user/([*]+)/data", UserDataHandler),
        (r'/game', GameHandler),
        (r"/game/([0-9]+)", GamePageHandler),
        (r'/game/([0-9]+)/data', GameDataHandler),
        (r'/game/([0-9]+)/move', MoveHandler),
        (r'/test', TestHandler),
    ], debug=True, cookie_secret='u5sJkk6UxCQB2X1CAehe7k9wxzBbrAFO9no3BoAT0Bu+zQabEnmXbwBtQCL5WbpPo/s=')

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
