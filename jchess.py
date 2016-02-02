import os, os.path
import sys

sys.path.append('./bin')
sys.path.append('./libraries/gson-2.5.jar')

from com.google.gson import Gson

from chessgame.Classes import ChessBoard

class ChessHandler(object):
    def __init__(self):
        self.board = ChessBoard()

    def getBoard(self):
        return self.board
