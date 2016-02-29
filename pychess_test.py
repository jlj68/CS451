import unittest
import pychess

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
 

class TestPychess(unittest.TestCase):
    def test_pawn(self):
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


if __name__ == '__main__':
    unittest.main()

