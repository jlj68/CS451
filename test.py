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
			self.assertEqual(king.color, pychess.Color.BLACK)
class TestKnight(unittest.TestCase):
	def runTest(self):
			knight = pychess.Knight(pychess.Color.BLACK)
			self.assertEqual(knight.color, pychess.Color.BLACK)
class TestPawn(unittest.TestCase):
	def runTest(self):
			pawn = pychess.Pawn(pychess.Color.BLACK)
			self.assertEqual(pawn.color, pychess.Color.BLACK)
class TestQueen(unittest.TestCase):
   def runTest(self):                                      
         queen = pychess.Queen(pychess.Color.BLACK)           
         self.assertEqual(queen.color, pychess.Color.BLACK)
class TestRook(unittest.TestCase):
   def runTest(self):
         rook = pychess.Rook(pychess.Color.BLACK)
         self.assertEqual(rook.color, pychess.Color.BLACK)
class TestPlayer(unittest.TestCase):
   def runTest(self):
         player = pychess.Player(pychess.Color.BLACK)
         self.assertEqual(player.color, pychess.Color.BLACK)
class TestGame(unittest.TestCase):
   def runTest(self):
         game = pychess.Game(pychess.Color.BLACK)
         self.assertEqual(game.color, pychess.Color.BLACK)
class TestChessBoard(unittest.TestCase):
   def runTest(self):
         chessBoard = pychess.ChessBoard(pychess.Color.BLACK)
         self.assertEqual(chessBoard.color, pychess.Color.BLACK)

