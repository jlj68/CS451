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
    def get(self):
        current_game = self.get_secure_cookie('current_game')
        if current_game:
            current_game = current_game.decode('ascii')
            self.render("./public/game.html", gameID=current_game, board=gamesList[int(current_game)].board.getBoardJson())
        else:
            self.render("./public/game.html", gameID=None)

    def put(self):
        current_game = self.get_secure_cookie('current_game')
        if current_game and int(current_game) in list(gamesList.keys()):
            raise tornado.web.HTTPError(403)
        gameID = random.randint(1, 1024)
        while gameID in gamesList.keys():
            gameID = random.randint(1, 1024)
        newGame = pychess.Game()
        gamesList[gameID] = newGame
        self.set_secure_cookie('current_game', str(gameID))
        self.write(tornado.escape.json_encode({'game_id': gameID, 'board': newGame.board.getBoardJson()}))
        #raise tornado.web.HTTPError(201)

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
        (r"/user", UserHandler),
        (r"/game", GameHandler),
    ], debug=True, cookie_secret='u5sJkk6UxCQB2X1CAehe7k9wxzBbrAFO9no3BoAT0Bu+zQabEnmXbwBtQCL5WbpPo/s=')

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
