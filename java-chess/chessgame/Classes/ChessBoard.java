package chessgame.Classes;
import java.util.HashMap;
import java.util.Map;

import chessgame.Classes.Pieces.*;

public class ChessBoard {
	
	Map<Position, Piece> board = new HashMap<Position, Piece>();
	
	public ChessBoard(){		
		board.put(new Position(0, 0), new Rook(Piece.Color.BLACK));
		board.put(new Position(0, 1), new Knight(Piece.Color.BLACK));
		board.put(new Position(0, 2), new Bishop(Piece.Color.BLACK));
		board.put(new Position(0, 3), new Queen(Piece.Color.BLACK));
		board.put(new Position(0, 4), new King(Piece.Color.BLACK));
		board.put(new Position(0, 5), new Bishop(Piece.Color.BLACK));
		board.put(new Position(0, 6), new Knight(Piece.Color.BLACK));
		board.put(new Position(0, 7), new Rook(Piece.Color.BLACK));
		
		board.put(new Position(1, 0), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 1), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 2), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 3), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 4), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 5), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 6), new Pawn(Piece.Color.BLACK));
		board.put(new Position(1, 7), new Pawn(Piece.Color.BLACK));
		
		board.put(new Position(6, 0), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 1), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 2), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 3), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 4), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 5), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 6), new Pawn(Piece.Color.WHITE));
		board.put(new Position(6, 7), new Pawn(Piece.Color.WHITE));
		
		board.put(new Position(7, 0), new Rook(Piece.Color.WHITE));
		board.put(new Position(7, 1), new Knight(Piece.Color.WHITE));
		board.put(new Position(7, 2), new Bishop(Piece.Color.WHITE));
		board.put(new Position(7, 3), new King(Piece.Color.WHITE));
		board.put(new Position(7, 4), new Queen(Piece.Color.WHITE));
		board.put(new Position(7, 5), new Bishop(Piece.Color.WHITE));
		board.put(new Position(7, 6), new Knight(Piece.Color.WHITE));
		board.put(new Position(7, 7), new Rook(Piece.Color.WHITE));
	}
	
	public Piece GetPiece(Position p){
		return board.get(p);
	}
	
	public void PrintBoard(){
		Piece[][] boardArray = new Piece[8][8];
		for(Position p : board.keySet()){
			boardArray[p.row][p.column] = board.get(p);
		}
		for(int i = 0; i < 8; i++){
			for(int j = 0; j < 8; j++){
				if(boardArray[i][j] == null)
					System.out.print("O ");
				else
					System.out.print(boardArray[i][j].pieceName.charAt(0) + " ");
			}
			System.out.println();
		}
	}
}
