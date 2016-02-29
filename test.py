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

class TestPawn(unittest.TestCase):
    def runTest(self):
        chessBoard = pychess.ChessBoard()
        testPosition = pychess.Position(1, 0)
        possibleMove =  chessBoard.getMovesFromPosition(testPosition)
        result = [
                pychess.Move(testPosition, pychess.Position(2, 0)),
                pychess.Move(testPosition, pychess.Position(3, 0))
            ]

        if len(possibleMove) != len(result):
            self.assertEqual(len(possibleMove), len(result))
            return

        flag = False
        for answer in result:
            for p in possibleMove:
                if compareMove(answer, p):
                    flag = True
            if not flag:
                self.assertEqual(1, 2)
                return
        self.assertEqual(1, 1)

                
def compareMove(move1, move2):
    if comparePosition(move1.fromPos, move2.fromPos) and comparePosition(move1.toPos, move2.toPos):
        return True
    return False

def comparePosition(position1, position2):
    if position1.row == position2.row and position1.col == position2.col:
        return True
    return False

class TestKnight(unittest.TestCase):
    def runTest(self):
        chessBoard = pychess.ChessBoard()
        testPosition = pychess.Position(0, 1)
        possibleMove =  chessBoard.getMovesFromPosition(testPosition)
        result = [
                pychess.Move(testPosition, pychess.Position(2, 0)),
                pychess.Move(testPosition, pychess.Position(2, 2))
            ]

        if len(possibleMove) != len(result):
            self.assertEqual(len(possibleMove), len(result))
            return

        flag = False
        for answer in result:
            for p in possibleMove:
                if compareMove(answer, p):
                    flag = True
            if not flag:
                self.assertEqual(1, 2)
                return
        self.assertEqual(1, 1)


def compareMove(move1, move2):
    if comparePosition(move1.fromPos, move2.fromPos) and comparePosition(move1.toPos, move2.toPos):
        return True
    return False

def comparePosition(position1, position2):
    if position1.row == position2.row and position1.col == position2.col:
        return True
    return False

def getTestBoard():
    chessBoard = pychess.ChessBoard()
    board = []
    for i in range(0, 8):
        row = []
        for j in range(0, 8):
            row.append(None)
        board.append(row)

    board[1][4] = pychess.King(pychess.Color.BLACK)
    board[2][5] = pychess.Pawn(pychess.Color.WHITE)
    board[3][0] = pychess.Pawn(pychess.Color.WHITE)
    board[3][2] = pychess.Rook(pychess.Color.BLACK)
    board[3][7] = pychess.Pawn(pychess.Color.BLACK)
    board[4][4] = pychess.Bishop(pychess.Color.BLACK)
    board[5][0] = pychess.Pawn(pychess.Color.BLACK)
    board[5][3] = pychess.Queen(pychess.Color.BLACK)
    board[5][6] = pychess.Knight(pychess.Color.BLACK)
    board[6][1] = pychess.Pawn(pychess.Color.WHITE)
    board[7][5] = pychess.Pawn(pychess.Color.WHITE)
    board[7][7] = pychess.Pawn(pychess.Color.WHITE)

    chessBoard.setBoard(board)
    return chessBoard        
