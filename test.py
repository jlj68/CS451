import unittest
import pychess

class TestChessMethods(unittest.TestCase):
    def runTest(self):
        cb = pychess.ChessBoard()
        self.assertEqual((len(cb.board[0]), len(cb.board)), (8, 8))

class TestBishop(unittest.TestCase):
    def runTest(self):
        bishop = pychess.Bishop(pychess.Color.BLACK)
        self.assertEqual(bishop.color, pychess.Color.BLACK)

class TestTemp(unittest.TestCase):
    def runTest(self):
        self.assertEqual(1, 1)
		
class TestHello(unittest.TestCase):
    def runTest(self):
        self.assertEqual(1, 1)

