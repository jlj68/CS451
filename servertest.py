import os, os.path
import string
import json
import sys
import jchess
import socket
import cherrypy

socket.IPPROTO_TCP = 6

class BasePage(object):
    @cherrypy.expose
    def index(self):
        return file('index.html')

class GetChessboard(object):
    exposed = True

    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def POST(self):
        ch = jchess.ChessHandler()
        cb = ch.getBoard().getBoardJson()
        print cb
        if cherrypy.request.json['username']:
            return {'valid': True}
        return {'valid': False}

    def GET(self):
        return "this is only a test"

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': '/home/alex/workspace/cs451-chessgame/public',
            'tools.staticdir.index': 'index.html'
        },
        '/board': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'application/json')]
        }
    }

    webapp = BasePage()
    webapp.board = GetChessboard()
    cherrypy.quickstart(webapp, '/', conf)
