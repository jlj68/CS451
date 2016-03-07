import unittest
import pychess
import pdb


def comparePosition(position1, position2):
    if position1.row == position2.row and position1.col == position2.col:
        return True
    return False


def compareMove(move1, move2):
    if comparePosition(move1.fromPos, move2.fromPos) and comparePosition(move1.toPos, move2.toPos):
        return True
    return False


def comparePossibleMoves(possible1, possible2):
    if len(possible1) != len(possible2):
        return False

    flag = False
    for move1 in possible1:
        for move2 in possible2:
            if compareMove(move1, move2):
                    flag = True
        if not flag:
            return False
    return True


def getTestBoard1():
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
 

def getTestBoard2():
    chessBoard = pychess.ChessBoard()
    board = []
    for i in range(0, 8):
        row = []
        for j in range(0, 8):
            row.append(None)
        board.append(row)

    board[0][0] = pychess.Rook(pychess.Color.BLACK)
    board[0][4] = pychess.King(pychess.Color.BLACK)

    chessBoard.setBoard(board)
    return chessBoard
 

def getTestBoard3():
    chessBoard = pychess.ChessBoard()
    board = []
    for i in range(0, 8):
        row = []
        for j in range(0, 8):
            row.append(None)
        board.append(row)

    board[4][4] = pychess.Pawn(pychess.Color.BLACK)
    board[4][4].hasMoved = True
    board[4][3] = pychess.Pawn(pychess.Color.WHITE)
    board[4][5] = pychess.Pawn(pychess.Color.WHITE)

    chessBoard.setBoard(board)
    return chessBoard


def getTestBoard4():
    chessBoard = pychess.ChessBoard()
    board = []
    for i in range(0, 8):
        row = []
        for j in range(0, 8):
            row.append(None)
        board.append(row)

    board[3][4] = pychess.Pawn(pychess.Color.WHITE)
    board[3][4].hasMoved = True
    board[3][3] = pychess.Pawn(pychess.Color.BLACK)
    board[3][5] = pychess.Pawn(pychess.Color.BLACK)

    chessBoard.setBoard(board)
    return chessBoard


def getPossibleMoves(testBoard, testPosition):
    possibleMove = testBoard.getMovesFromPosition(testPosition)
    return possibleMove
    

class TestPychess(unittest.TestCase):
    def test_king(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(1, 4)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(0, 3)),
                pychess.Move(testPosition, pychess.Position(0, 4)),
                pychess.Move(testPosition, pychess.Position(0, 5)),
                pychess.Move(testPosition, pychess.Position(1, 3)),
                pychess.Move(testPosition, pychess.Position(1, 5)),
                pychess.Move(testPosition, pychess.Position(2, 3)),
                pychess.Move(testPosition, pychess.Position(2, 4)),
                pychess.Move(testPosition, pychess.Position(2, 5))
            ]
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_queen(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(5, 3)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(0, 3)),
                pychess.Move(testPosition, pychess.Position(1, 3)),
                pychess.Move(testPosition, pychess.Position(2, 3)),
                pychess.Move(testPosition, pychess.Position(3, 3)),
                pychess.Move(testPosition, pychess.Position(4, 3)),
                pychess.Move(testPosition, pychess.Position(6, 3)),
                pychess.Move(testPosition, pychess.Position(7, 3)),
                
                pychess.Move(testPosition, pychess.Position(5, 1)),
                pychess.Move(testPosition, pychess.Position(5, 2)),
                pychess.Move(testPosition, pychess.Position(5, 4)),
                pychess.Move(testPosition, pychess.Position(5, 5)),
                
                pychess.Move(testPosition, pychess.Position(2, 0)),
                pychess.Move(testPosition, pychess.Position(3, 1)),
                pychess.Move(testPosition, pychess.Position(4, 2)),
                pychess.Move(testPosition, pychess.Position(6, 4)),
                pychess.Move(testPosition, pychess.Position(7, 5)),
                
                pychess.Move(testPosition, pychess.Position(6, 2)),
                pychess.Move(testPosition, pychess.Position(7, 1))
            ]
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_pawn(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(5, 0)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(6, 0)),
                pychess.Move(testPosition, pychess.Position(7, 0)),
                pychess.Move(testPosition, pychess.Position(6, 1))
            ]
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_knight(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(5, 6)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(3, 5)),
                pychess.Move(testPosition, pychess.Position(7, 5)),
                pychess.Move(testPosition, pychess.Position(7, 7)),
                pychess.Move(testPosition, pychess.Position(6, 4))
            ]
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_rook(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(3, 2)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(3, 0)),
                pychess.Move(testPosition, pychess.Position(3, 1)),
                pychess.Move(testPosition, pychess.Position(3, 3)),
                pychess.Move(testPosition, pychess.Position(3, 4)),
                pychess.Move(testPosition, pychess.Position(3, 5)),
                pychess.Move(testPosition, pychess.Position(3, 6)),
                pychess.Move(testPosition, pychess.Position(0, 2)),
                pychess.Move(testPosition, pychess.Position(1, 2)),
                pychess.Move(testPosition, pychess.Position(2, 2)),
                pychess.Move(testPosition, pychess.Position(4, 2)),
                pychess.Move(testPosition, pychess.Position(5, 2)),
                pychess.Move(testPosition, pychess.Position(6, 2)),
                pychess.Move(testPosition, pychess.Position(7, 2))
            ]
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_bishop(self):
        testBoard = getTestBoard1()
        testPosition = pychess.Position(4, 4)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(0, 0)),
                pychess.Move(testPosition, pychess.Position(1, 1)),
                pychess.Move(testPosition, pychess.Position(2, 2)),
                pychess.Move(testPosition, pychess.Position(3, 3)),
                pychess.Move(testPosition, pychess.Position(5, 5)),
                pychess.Move(testPosition, pychess.Position(6, 6)),
                pychess.Move(testPosition, pychess.Position(7, 7)),
                
                pychess.Move(testPosition, pychess.Position(3, 5)),
                pychess.Move(testPosition, pychess.Position(2, 6)),
                pychess.Move(testPosition, pychess.Position(1, 7))
            ]
        # pdb.set_trace()
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_castling(self):
        testBoard = getTestBoard2()
        testPosition = pychess.Position(0, 4)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(0, 3)),
                pychess.Move(testPosition, pychess.Position(0, 5)),
                pychess.Move(testPosition, pychess.Position(1, 3)),
                pychess.Move(testPosition, pychess.Position(1, 4)),
                pychess.Move(testPosition, pychess.Position(1, 5)),
                pychess.Move(testPosition, pychess.Position(0, 0)),
            ]
        # pdb.set_trace()
        self.assertTrue(comparePossibleMoves(possibleMove, answer))


    def test_En_passant_black(self):
        testBoard = getTestBoard3()
        testPosition = pychess.Position(4, 4)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(5, 4)),
                pychess.Move(testPosition, pychess.Position(4, 3)),
                pychess.Move(testPosition, pychess.Position(4, 5))
            ]
        # pdb.set_trace()
        self.assertTrue(comparePossibleMoves(possibleMove, answer))
        

    def test_En_passant_white(self):
        testBoard = getTestBoard4()
        testPosition = pychess.Position(3, 4)
        possibleMove = getPossibleMoves(testBoard, testPosition)
        answer = [
                pychess.Move(testPosition, pychess.Position(2, 4)),
                pychess.Move(testPosition, pychess.Position(3, 3)),
                pychess.Move(testPosition, pychess.Position(3, 5))
            ]
        # pdb.set_trace()
        self.assertTrue(comparePossibleMoves(possibleMove, answer))



if __name__ == '__main__':
    unittest.main()

