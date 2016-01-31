import os, os.path
import string
import json

import cherrypy
from chessgame.Classes import ChessBoard

class BasePage(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')

class GetChessboard(object):
    exposed = True

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        cb = ChessBoard()
        return cb.board
        #return json.dumps({'username': 'test_user'})

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '/home/alex/workspace/cs451-chessgame/java-chess/webserver/public',
            'tools.staticdir.index': 'index.html'
        },
        '/board': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        }
    }

    webapp = BasePage()
    webapp.board = GetChessboard()
    cherrypy.quickstart(webapp, '/', conf)
