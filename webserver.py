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

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./public/index.html")

class GameHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("./public/game.html")

    def put(self):
        gameID = random.randint(1, 1024)
        while gameID in gamesList.keys():
            gameID = random.randint(1, 1024)
        gamesList[gameID] = pychess.Game()
        self.write(tornado.escape.json_encode({'game_id': gameID, 'board': gamesList[gameID].board.getBoardJson()}))
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
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
