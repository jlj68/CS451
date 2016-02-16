import tornado.ioloop
import tornado.web
import tornado.websocket
import json
from user import User
import pychess
import random

gamesList = {}
activeUsers = {}
availableUsers = {}

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
        self.write(tornado.escape.json_encode({'gameID': str(gameID) }))

class GamePageHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.render("./public/game.html", gameID=id)

class GameDataHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(tornado.escape.json_encode({'board': gamesList[int(id)].board.getBoardJson()}))

class MoveHandler(tornado.web.RequestHandler):
    def get(self, id):
        # get moves from a position
        row = int(self.get_argument('row'))
        col = int(self.get_argument('col'))
        moves = gamesList[int(id)].board.getMovesFromPosition(row, col)
        movesList = [{'fromPos': move.fromPos.__dict__, 'toPos': move.toPos.__dict__} for move in moves]
        self.write(tornado.escape.json_encode({ 'moves': movesList }))

    def put(self, id):
        originPosition = pychess.Position(int(self.get_body_argument('fromPosRow')), int(self.get_body_argument('fromPosCol')))
        destPosition = pychess.Position(int(self.get_body_argument('toPosRow')), int(self.get_body_argument('toPosCol')))
        gamesList[int(id)].board.applyMove(pychess.Move(originPosition, destPosition))
        raise tornado.web.HTTPError(200)

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
            raise tornado.web.HTTPError(201)
        else:
            raise tornado.web.HTTPError(409)

    def post(self):
        self.write("modifying user")

class UserDataHandler(tornado.web.RequestHandler):
    def get(self, username):
        self.write(tornado.escape.json_encode({'user_data': activeUsers[username].__dict__}))

class MySocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Socket opened.")

    def on_message(self, message):
        print(message)

    def on_close(self):
        print("Socket closed")

def make_app():
    return tornado.web.Application([
        (r'/public/(.*)', tornado.web.StaticFileHandler, {'path': './public/'}),
        (r"/", MainHandler),
        (r"/ws", MySocketHandler),
        (r"/users", UserHandler),
        (r"/user/([*]+)/data", UserDataHandler),
        (r'/game', GameHandler),
        (r"/game/([0-9]+)", GamePageHandler),
        (r'/game/([0-9]+)/data', GameDataHandler),
        (r'/game/([0-9]+)/move', MoveHandler),
    ], debug=True, cookie_secret='u5sJkk6UxCQB2X1CAehe7k9wxzBbrAFO9no3BoAT0Bu+zQabEnmXbwBtQCL5WbpPo/s=')

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
