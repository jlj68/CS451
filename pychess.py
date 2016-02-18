from enum import Enum, unique
from abc import ABCMeta, abstractmethod
import os, sys

@unique
class State(Enum):
    MATCH = 1
    DRAW = 2
    BLACK_WIN = 3
    WHITE_WIN = 4
    BLACK_CHECK = 5
    WHITE_CHECK = 6
    BLACK_CHECKMATE = 7
    WHITE_CHECKMATE = 8


@unique
class Color(Enum):
    BLACK = 1
    WHITE = 2


class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
        return "(" + str(self.row) + ", " + str(self.col) + ")"


class Move:
    def __init__(self, fromPos, toPos):
        self.fromPos = fromPos
        self.toPos = toPos

    def __str__(self):
        return str(self.fromPos) + "->" + str(self.toPos)


class Piece:
    __metaclass__ = ABCMeta

    def __init__(self, name, ch, color):
        self.name = name
        self.ch = ch
        self.color = color
        self.hasMoved = False

    def __str__(self):
        return str(self.color)[6] + self.ch

    @abstractmethod
    def getPossibleMoves(self, position, board): pass

    def filterPositions(self, board, current, delta):
        destination = []

        current = Position(current.row+delta.row, current.col+delta.col)
        while current.row < 8 and current.row > -1 and current.col < 8 and current.col > -1:
            piece = board[current.row][current.col]
            if piece is None:
                destination.append(current)
            elif piece.color != self.color:
                destination.append(current)
                break
            else:
                break

            current = Position(current.row+delta.row, current.col+delta.col)

        return destination

    def getFilterPositions(self, board, current, directions):
        destination = []
        for d in directions:
            destination += self.filterPositions(board, current, d)
        return destination


class Bishop(Piece):
    def __init__(self, color):
        super(Bishop, self).__init__("Bishop", "B", color)

    def getPossibleMoves(self, position, board):
        directions = [
            Position(1, 1),
            Position(1, -1),
            Position(-1, 1),
            Position(-1, -1),
        ]

        destinations = super(Bishop, self).getFilterPositions(board, position, directions)
        positions = []

        for pos in destinations:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions


class King(Piece):
    def __init__(self, color):
        super(King, self).__init__("King", "K", color)

    def getPossibleMoves(self, position, board):
        positions = [
            Position(position.row+1, position.col),
            Position(position.row-1, position.col),
            Position(position.row, position.col+1),
            Position(position.row, position.col-1),
            Position(position.row+1, position.col+1),
            Position(position.row-1, position.col+1),
            Position(position.row+1, position.col-1),
            Position(position.row-1, position.col-1),
        ]

        destinations = []

        for i in range(0, len(positions)):
            if positions[i].row in range(0, 8) and positions[i].col in range(0, 8):
                piece = board[positions[i].row][positions[i].col]
                if piece is None or piece.color is not self.color:
                    destinations.append(positions[i])

        possiblePositions = []

        for pos in destinations:
            if pos.row in range(0, 8) and pos.col in range(0, 8):
                possiblePositions.append(Move(position, pos))

        return possiblePositions


class Knight(Piece):
    def __init__(self, color):
        super(Knight, self).__init__("Knight", "N", color)

    def getPossibleMoves(self, position, board):
        positions = [
            Position(position.row+2, position.col+1),
            Position(position.row+2, position.col-1),
            Position(position.row-2, position.col+1),
            Position(position.row-2, position.col-1),
            Position(position.row+1, position.col+2),
            Position(position.row-1, position.col+2),
            Position(position.row+1, position.col-2),
            Position(position.row-1, position.col-2),
        ]

        destinations = []

        for i in range(0, len(positions)):
            if positions[i].row in range(0, 8) and positions[i].col in range(0, 8):
                piece = board[positions[i].row][positions[i].col]
                if piece is None or piece.color is not self.color:
                    destinations.append(positions[i])

        possiblePositions = []

        for p in destinations:
            if p.row in range(1, 7) or p.col in range(1, 7):
                possiblePositions.append(Move(position, p))

        return possiblePositions


class Pawn(Piece):
    def __init__(self, color):
        super(Pawn, self).__init__("Pawn", "P", color)

    def getPossibleMoves(self, position, board):
        possiblePositions = []
        direction = 1 if self.color is Color.BLACK else -1
        destinations = [
            Position(position.row+direction, position.col+1),
            Position(position.row+direction, position.col-1),
        ]

        for p in destinations:
            if p.row in range(0, 8) and p.col in range(0, 8):
                piece = board[p.row][p.col]
                if piece is not None and piece.color is not self.color:
                    possiblePositions.append(Move(position, p))

        destinations = []
        if not self.hasMoved:
            destinations.append(Position(position.row+2*direction, position.col))
        destinations.append(Position(position.row+direction, position.col))

        for p in destinations:
            if p.row in range(0, 8) and p.col in range(0, 8):
                piece = board[p.row][p.col]
                if piece is None:
                    possiblePositions.append(Move(position, p))

        return possiblePositions


class Queen(Piece):
    def __init__(self, color):
        super(Queen, self).__init__("Queen", "Q", color)

    def getPossibleMoves(self, position, board):
        directions = [
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
        ]

        destinations = super(Queen, self).getFilterPositions(board, position, directions)
        positions = []

        for pos in destinations:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions


class Rook(Piece):
    def __init__(self, color):
        super(Rook, self).__init__("Rook", "R", color)

    def getPossibleMoves(self, position, board):
        directions = [
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
        ]

        destination = super(Rook, self).getFilterPositions(board, position, directions)
        positions = []

        for pos in destination:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions


class Player:
    def __init__(self, color):
        self.playerColor = color

    def getMove(self, game):
        moves = game.getPossibleMoves()
        allMoves = []

        i = 1

        for position in moves.keys():
            tmp = moves.get(position)
            for move in tmp:
                allMoves.append(move)
                print(str(i) + ". " + str(move))
                i += 1

        print("Select a move: ", "")
        moveSelection = input()

        return allMoves[int(moveSelection)-1]


class Game:
    def __init__(self):
        self.board = ChessBoard()
        self.current = Color.BLACK

    def displayGame(self):
        print("Game State: " + str(self.board.state.name))
        print("Current player: " + str(self.current.name))
        print(str(self.board))

    def isGameOver(self):
        return self.board.state in [State.DRAW, State.BLACK_WIN, State.WHITE_WIN]

    def getPossibleMoves(self):
        return self.board.getPossibleMoves(self.current)

    def applyMove(self, move):
        self.board.applyMove(move)
        self.current = Color.BLACK if self.current is Color.WHITE else Color.WHITE

    def getState(self):
        return self.board.state;


class ChessBoard:
    def __init__(self):
        self.state = State.MATCH
        self.board = []
        for i in range(0, 8):
            row = []
            for j in range(0, 8):
                row.append(None)
            self.board.append(row)

        self.board[0][0] = Rook(Color.BLACK)
        self.board[0][1] = Knight(Color.BLACK)
        self.board[0][2] = Bishop(Color.BLACK)
        self.board[0][3] = Queen(Color.BLACK)
        self.board[0][4] = King(Color.BLACK)
        self.board[0][5] = Bishop(Color.BLACK)
        self.board[0][6] = Knight(Color.BLACK)
        self.board[0][7] = Rook(Color.BLACK)

        self.board[1][0] = Pawn(Color.BLACK)
        self.board[1][1] = Pawn(Color.BLACK)
        self.board[1][2] = Pawn(Color.BLACK)
        self.board[1][3] = Pawn(Color.BLACK)
        self.board[1][4] = Pawn(Color.BLACK)
        self.board[1][5] = Pawn(Color.BLACK)
        self.board[1][6] = Pawn(Color.BLACK)
        self.board[1][7] = Pawn(Color.BLACK)


        self.board[6][0] = Pawn(Color.WHITE)
        self.board[6][1] = Pawn(Color.WHITE)
        self.board[6][2] = Pawn(Color.WHITE)
        self.board[6][3] = Pawn(Color.WHITE)
        self.board[6][4] = Pawn(Color.WHITE)
        self.board[6][5] = Pawn(Color.WHITE)
        self.board[6][6] = Pawn(Color.WHITE)
        self.board[6][7] = Pawn(Color.WHITE)

        self.board[7][0] = Rook(Color.WHITE)
        self.board[7][1] = Knight(Color.WHITE)
        self.board[7][2] = Bishop(Color.WHITE)
        self.board[7][3] = King(Color.WHITE)
        self.board[7][4] = Queen(Color.WHITE)
        self.board[7][5] = Bishop(Color.WHITE)
        self.board[7][6] = Knight(Color.WHITE)
        self.board[7][7] = Rook(Color.WHITE)

    def setBoard(self, board):
        self.board = board;

    def getPiece(self, position):
        if p.row in range(0, 8) and p.col in range(0, 8):
            return self.board[p.row][p.col]
        return None

    def getPossibleMoves(self, color):
        moves = {}

        for i in range(0, 8):
            for j in range(0, 8):
                p = Position(i, j)
                piece = self.board[i][j]
                if piece is not None and piece.color == color:
                    moves[p] = piece.getPossibleMoves(p, self.board)

        return moves

    def getMovesFromPosition(self, position):
        piece = self.board[position.row][position.col]
        if piece is not None:
            return piece.getPossibleMoves(position, self.board)
        else:
            return []

    def isValidMove(self, move):
        return True if move in getPossibleMoves(self.current) else False

    def applyMove(self, move):
        fromPiece = self.board[move.fromPos.row][move.fromPos.col]
        toPiece = self.board[move.toPos.row][move.toPos.col]

        self.board[move.fromPos.row][move.fromPos.col] = None
        self.board[move.toPos.row][move.toPos.col] = fromPiece

        fromPiece.hasMoved = True

        if toPiece is not None and toPiece.name == "King":
            self.state = State.WHITE_WIN if toPiece.color is Color.BLACK else State.BLACK_WIN
        else:
            opponentColor = Color.BLACK if fromPiece.color is Color.WHITE else Color.WHITE
            self.checkState(opponentColor)

    def findKing(self, color):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                piece = self.board[i][j]
                if piece != None and piece.name == "King" and piece.color == color:
                    return Position(i, j)
        return None

    def checkState(self, color):
        self.state = State.MATCH
        if self.isCheck(color):
            self.state = State.BLACK_CHECK if color is Color.BLACK else State.WHITE_CHECK
            if self.isCheckmate(color):
                self.state = State.BLACK_CHECKMATE if color is Color.BLACK else State.WHITE_CHECKMATE


    def isCheck(self, color):
        opponentColor = Color.BLACK if color is Color.WHITE else Color.WHITE
        kingPosition = self.findKing(color)
        possibleMoves = self.getPossibleMoves(opponentColor)

        for key in possibleMoves.keys():
            for m in possibleMoves.get(key):
                p = m.toPos;
                if(p.row == kingPosition.row and p.col == kingPosition.col):
                    return True
        return False


    def isCheckmate(self, color):
        opponentColor = Color.BLACK if color is Color.WHITE else Color.WHITE
        kingPosition = self.findKing(color)
        kingPossibleMoves = self.getMovesFromPosition(kingPosition)
        possibleMoves = self.getPossibleMoves(opponentColor)

        targeted = []
        for km in kingPossibleMoves:
            kp = km.toPos
            for key in possibleMoves.keys():
                for m in possibleMoves.get(key):
                    p = m.toPos
                    if(p.row == kp.row and p.col == kp.col and kp not in targeted):
                        targeted.append(kp)

        if len(targeted) == len(kingPossibleMoves):
            return True
        return False


    def __str__(self):
        boardString = "     0   1   2   3   4   5   6   7\n"
        for i in range(len(self.board)):
            boardString += " " + str(i)
            for j in range(len(self.board[i])):
                piece = self.board[i][j];
                if piece is None:
                    boardString += "  --"
                else:
                    boardString += "  " + piece.__str__();
            boardString += "\n"
        return boardString

    def getBoardJson(self):
        board = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.board[i][j] is not None:
                    elem = self.board[i][j].__dict__.copy()
                    elem['color'] = elem['color'].name
                else:
                    elem = None
                board.append({'row': i, 'col': j, 'piece': elem})
        return board


if __name__ == "__main__":
    game = Game()

    player1 = Player(Color.WHITE)
    player2 = Player(Color.BLACK)

    while not game.isGameOver():
        game.displayGame()
        print("")
        move = player2.getMove(game) if game.current is Color.BLACK else player1.getMove(game)
        game.applyMove(move)

    print(game.getState())
