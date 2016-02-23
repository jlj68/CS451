import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from user import User, UserStatus
import pychess
import random

# {id: (game, whitePlayerWebsocket, blackPlayerWebsocket)}
gamesList = {}

connectedUsers = {}
websocketClients = {}

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

# this, too
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
        for user in connectedUsers.keys():
            elem = connectedUsers[user].__dict__.copy()
            elem['status'] = elem['status'].name
            userList.append(elem)
        userList = sorted(userList, key = lambda user: user['username'])
        self.write(tornado.escape.json_encode({'users': userList}))

    def put(self):
        username = self.get_body_argument("username")
        if username not in connectedUsers.keys():
            newUser = User(username)
            connectedUsers[username] = newUser
            self.set_secure_cookie('username', username)
            raise tornado.web.HTTPError(201)
        else:
            raise tornado.web.HTTPError(409)

    def post(self):
        self.write("modifying user")

class UserDataHandler(tornado.web.RequestHandler):
    def get(self, username):
        self.write(tornado.escape.json_encode({'user_data': connectedUsers[username].__dict__}))

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
            if connectedUsers[messageDict['target']].status is UserStatus.AVAILABLE:
                connectedUsers[messageDict['target']].status = UserStatus.PENDING_INVITE
                websocketClients[messageDict['target']].write_message(tornado.escape.json_encode({'sender': self.get_secure_cookie('username').decode('ascii')}))
            else:
                self.write_message(tornado.escape.json_encode({'status': 'failed'}))
        elif messageDict['function'] == "receive":
            websocketClients[messageDict['sender']].status = UserStatus.PENDING_INVITE
            websocketClients[messageDict['sender'].decode('ascii')].write_message(tornado.escape.json_encode({'request': 'invited'}))
        elif messageDict['function'] == "accept":
            connectedUsers[messageDict['sender']].status = UserStatus.IN_GAME
            connectedUsers[messageDict['target']].status = UserStatus.IN_GAME
            websocketClients[messageDict['target']].write_message(tornado.escape.json_encode({'function': 'joining_game'}))
            self.write_message(tornado.escape.json_encode({'function': 'create_game'}))
        elif messageDict['function'] == "decline":
            connectedUsers[messageDict['sender']].status = UserStatus.AVAILABLE
            connectedUsers[messageDict['target']].status = UserStatus.AVAILABLE

    def on_close(self):
        del websocketClients[self.get_secure_cookie('username').decode('ascii')]
        print("Socket closed")

class GameSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        for (key, values) in gamesList.items():
            if self.get_secure_cookie('username') in values:
                values[values.index(self.get_secure_cookie('username'))] = self
                break
        print("not found!")



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
