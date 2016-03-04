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
        player1 = self.get_secure_cookie('username')
        player2 = self.get_body_argument('player2')
        gamesList[gameID] = [newGame, player1, player2]
        self.set_secure_cookie('gameID', str(gameID))
        self.set_secure_cookie('player_color', 'BLACK')
        websocketClients[player2].write_message(tornado.escape.json_encode({'function': 'joining_game', 'gameID': gameID}))
        self.write(tornado.escape.json_encode({'gameID': gameID}))

class GamePageHandler(tornado.web.RequestHandler):
    def get(self, gameID):
        if not self.get_secure_cookie('player_color'):
            self.set_secure_cookie('player_color', 'BLACK')
            self.set_secure_cookie('gameID', str(gameID))
        self.render("./public/game.html", gameID=gameID)

# this will be a web socket class
class GameDataHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write(tornado.escape.json_encode({'board': gamesList[int(id)][0].board.getBoardJson()}))

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
        print("socket opened")

    def on_message(self, message):
        messageDict = tornado.escape.json_decode(message)
        if messageDict['function'] == "send":
            if connectedUsers[messageDict['target']].status is UserStatus.AVAILABLE:
                connectedUsers[messageDict['target']].status = UserStatus.PENDING_INVITE
                websocketClients[messageDict['target']].write_message(tornado.escape.json_encode({'sender': self.get_secure_cookie('username').decode('ascii')}))
                self.write_message(tornado.escape.json_encode({'status': 'success'}))
            else:
                self.write_message(tornado.escape.json_encode({'status': 'failed'}))
        elif messageDict['function'] == "receive":
            websocketClients[messageDict['sender']].status = UserStatus.PENDING_INVITE
            websocketClients[messageDict['sender'].decode('ascii')].write_message(tornado.escape.json_encode({'request': 'invited'}))
        elif messageDict['function'] == "accept":
            connectedUsers[messageDict['sender'].decode('ascii')].status = UserStatus.IN_GAME
            connectedUsers[messageDict['target']].status = UserStatus.IN_GAME
            websocketClients[messageDict['target']].write_message(tornado.escape.json_encode({'function': 'joining_game'}))
            self.write_message(tornado.escape.json_encode({'function': 'create_game'}))
        elif messageDict['function'] == "decline":
            connectedUsers[messageDict['sender'].decode('ascii')].status = UserStatus.AVAILABLE
            connectedUsers[messageDict['target']].status = UserStatus.AVAILABLE
        elif messageDict['function'] == "register":
            websocketClients[messageDict['name']] = self

    def close(self):
        del websocketClients[self.get_secure_cookie('username').decode('ascii')]
        print("Socket closed")

class GameSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        for key, values in gamesList.items():
            if self.get_secure_cookie('username') in values:
                values[values.index(self.get_secure_cookie('username'))] = self
                break

    def on_message(self, clientMessage):
        message = tornado.escape.json_decode(clientMessage)
        gameID = int(self.get_secure_cookie('gameID'))
        gameBoard = gamesList[gameID][0].board

        if message['function'] == 'get_moves':
            print(gameBoard.getPossibleMovesJSON(pychess.Color.fromString(self.get_secure_cookie('player_color').decode('ascii'))))
            self.write_message(tornado.escape.json_encode(gameBoard.getPossibleMovesJSON(pychess.Color.fromString(self.get_secure_cookie('player_color').decode('ascii')))))
        elif message['function'] == 'make_move':
            fromPos = pychess.Position(message['move']['fromPos']['row'], message['move']['fromPos']['col'])
            toPos = pychess.Position(message['move']['toPos']['row'], message['move']['toPos']['col'])
            move = pychess.Move(fromPos, toPos)
            if gameBoard.isValidMove(move, pychess.Color.fromString(self.get_secure_cookie('player_color').decode('ascii'))):
                gameBoard.applyMove(move)
                gamesList[gameID][1].write_message(tornado.escape.json_encode({'state': gameBoard.state.name, 'board': gameBoard.getBoardJson()}))
                gamesList[gameID][2].write_message(tornado.escape.json_encode({'state': gameBoard.state.name, 'board': gameBoard.getBoardJson()}))
            else:
                self.write_message(tornado.escape.json_encode({'function': 'error', 'status': 'invalid_move'}))
        elif message['function'] == 'update_board':
            self.write_message(tornado.escape.json_encode({'state': gameBoard.state.name, 'board': gameBoard.getBoardJson()}))

    def close(self):
        for key, values in gamesList.items():
            if self.get_secure_cookie('username') == value:
                del values[values.index(self)]
                self.write_message(tornado.escape.json_encode({'status': 'disconnected', 'username': value}))
                break

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
        (r'/game/socket', GameSocketHandler),
        (r'/test', TestHandler),
    ], debug=True, cookie_secret='u5sJkk6UxCQB2X1CAehe7k9wxzBbrAFO9no3BoAT0Bu+zQabEnmXbwBtQCL5WbpPo/s=')

if __name__ == "__main__":
    app = make_app()
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()
