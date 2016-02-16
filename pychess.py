from enum import Enum, unique
from abc import ABCMeta, abstractmethod
import os, sys

@unique
class State(Enum):
    MATCH = 1
    DRAW = 2
    BLACKWIN = 3
    WHITEWIN = 4

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

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.hasMoved = False

    def __str__(self):
        return str(self.color)[0] + self.name[0]

    @abstractmethod
    def possibleMoves(self, position, board): pass

    def filterPositions(self, board, current, delta):
        destination = []
        tempPosition = Position(current.row+delta.row, current.col+delta.col)

        while current.row < 8 and current.row > -1 and current.col < 8 and current.col > -1:
            piece = board[current.row][current.col]
            if piece is None or piece.color != self.color:
                destination.append(current)
                break
            else:
                break

            current = Position(current.row+delta.row, current.col+delta.col)

        return destination

    def getFilterPositions(self, board, current, delta):
        destination = []

        for i in range(0, len(delta)):
            path = self.filterPositions(board, current, delta[i])
            for j in range(0, len(path)):
                destination.append(path[j])

        return destination

class Bishop(Piece):
    def __init__(self, color):
        super(Bishop, self).__init__("Bishop", color)

    def possibleMoves(self, position, board):
        delta = [
            Position(1, 1),
            Position(1, -1),
            Position(-1, 1),
            Position(-1, -1),
        ]

        destinations = super(Bishop, self).getFilterPositions(board, position, delta)
        positions = []

        for pos in destinations:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions

class King(Piece):
    def __init__(self, color):
        super(King, self).__init__("King", color)

    def possibleMoves(self, position, board):
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
        super(Knight, self).__init__("Knight", color)

    def possibleMoves(self, position, board):
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
        super(Pawn, self).__init__("Pawn", color)

    def possibleMoves(self, position, board):
        destinations = []
        direction = 1 if self.color is Color.BLACK else -1

        positions = [
            Position(position.row+direction, position.col+1),
            Position(position.row+direction, position.col-1),
        ]

        for i in range(0, len(positions)):
            if positions[i].row in range(0, 8) and positions[i].col in range(0, 8):
                piece = board[positions[i].row][positions[i].col]
                if piece is not None and piece.color is not self.color:
                    destinations.append(positions[i])

        pos = []

        if not self.hasMoved:
            pos.append(Position(position.row+2*direction, position.col))
        pos.append(Position(position.row+direction, position.col))

        for i in range(0, len(pos)):
            piece = board[pos[i].row][pos[i].col]
            if piece is None:
                destinations.append(pos[i])

        possiblePositions = []

        for p in destinations:
            if p.row in range(0, 8) or p.col in range(0, 8):
                possiblePositions.append(Move(position, p))

        return possiblePositions

class Queen(Piece):
    def __init__(self, color):
        super(Queen, self).__init__("Queen", color)

    def possibleMoves(self, position, board):
        delta = [
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
        ]

        destinations = super(Queen, self).getFilterPositions(board, position, delta)
        positions = []

        for pos in destinations:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions

class Rook(Piece):
    def __init__(self, color):
        super(Rook, self).__init__("Rook", color)

    def possibleMoves(self, position, board):
        delta = [
            Position(1, 0),
            Position(-1, 0),
            Position(0, 1),
            Position(0, -1),
        ]

        destination = super(Rook, self).getFilterPositions(board, position, delta)
        positions = []

        for pos in destination:
            if pos.row in range(1, 7) or pos.col in range(1, 7):
                positions.append(Move(position, pos))

        return positions

class Player:
    def __init__(self, color):
        self.playerColor = color

    def getMove(self, game):
        moves = game.generateMoves()
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
        print("Current player: " + str(self.current.name))
        print(str(self.board))

    def isGameOver(self):
        return self.board.state is State.MATCH

    def generateMoves(self):
        return self.board.generateMoves(self.current)

    def applyMove(self, move):
        self.board.applyMove(move)
        self.current = Color.BLACK if self.current is Color.WHITE else Color.WHITE

class ChessBoard:
    def __init__(self):
        self.state = None
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

    def getPiece(self, position):
        if p.row in range(0, 8) and p.col in range(0, 8):
            return self.board[p.row][p.col]
        return None

    def generateMoves(self, color):
        moves = {}

        for i in range(0, 8):
            for j in range(0, 8):
                p = Position(i, j)
                piece = self.board[i][j]
                if piece is not None and piece.color == color:
                    moves[p] = piece.possibleMoves(p, self.board)

        return moves

    def getMovesFromPosition(self, row, col):
        if self.board[row][col] is not None:
            allMoves = self.generateMoves(self.board[row][col].color)
            for position in list(allMoves.keys()):
                if position.row == row and position.col == col:
                    return allMoves[position]
        else:
            return []

    def applyMove(self, move):
        fromPiece = self.board[move.fromPos.row][move.fromPos.col]
        toPiece = self.board[move.toPos.row][move.toPos.col]

        self.board[move.fromPos.row][move.fromPos.col] = None
        self.board[move.toPos.row][move.toPos.col] = fromPiece

        fromPiece.hasMoved = True

        if toPiece is not None and toPiece.name == "King":
            self.state = State.WHITEWIN if toPiece.color is Color.BLACK else State.BLACKWIN

    def __str__(self):
        boardString = "  0 1 2 3 4 5 6 7\n"
        for i in range(0, 8):
            boardString += str(i) + " "
            for j in range(0, 8):
                if self.board[i][j] is None:
                    boardString += "- "
                else:
                    boardString += self.board[i][j].name[0] + " "
            boardString += '\n'
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
'''

if __name__ == "__main__":
    game = Game()

    player1 = Player(Color.WHITE)
    player2 = Player(Color.BLACK)

    while not game.isGameOver():
        game.displayGame()
        print("")
        move = player2.getMove(game) if game.current is Color.BLACK else player1.getMove(game)
        game.applyMove(move)

    print(game.state.name)
'''
