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

class TestKing(unittest.TestCase):
	def runTest(self):
			king = pychess.King(pychess.Color.BLACK)
			self.assertEqual(king.color, pychess.Color.WHITE)
			
