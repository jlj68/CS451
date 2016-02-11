import unittest
import pychess

class TestChessMethods(unittest.TestCase):
        def runTest(self):
            cb = pychess.ChessBoard()
            self.assertEqual((len(cb.board[0]), len(cb.board)), (8, 8))
