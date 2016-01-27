package chessgame.Classes;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import chessgame.Classes.Pieces.*;

public class ChessBoard {
	
	Map<Position, Piece> board = new HashMap<Position, Piece>();
	public State state = State.MATCH;
	
	public ChessBoard() {
		board.put(new Position(0, 0), new Rook(Color.BLACK));
		board.put(new Position(0, 1), new Knight(Color.BLACK));
		board.put(new Position(0, 2), new Bishop(Color.BLACK));
		board.put(new Position(0, 3), new Queen(Color.BLACK));
		board.put(new Position(0, 4), new King(Color.BLACK));
		board.put(new Position(0, 5), new Bishop(Color.BLACK));
		board.put(new Position(0, 6), new Knight(Color.BLACK));
		board.put(new Position(0, 7), new Rook(Color.BLACK));
		
		board.put(new Position(1, 0), new Pawn(Color.BLACK));
		board.put(new Position(1, 1), new Pawn(Color.BLACK));
		board.put(new Position(1, 2), new Pawn(Color.BLACK));
		board.put(new Position(1, 3), new Pawn(Color.BLACK));
		board.put(new Position(1, 4), new Pawn(Color.BLACK));
		board.put(new Position(1, 5), new Pawn(Color.BLACK));
		board.put(new Position(1, 6), new Pawn(Color.BLACK));
		board.put(new Position(1, 7), new Pawn(Color.BLACK));
		
		board.put(new Position(6, 0), new Pawn(Color.WHITE));
		board.put(new Position(6, 1), new Pawn(Color.WHITE));
		board.put(new Position(6, 2), new Pawn(Color.WHITE));
		board.put(new Position(6, 3), new Pawn(Color.WHITE));
		board.put(new Position(6, 4), new Pawn(Color.WHITE));
		board.put(new Position(6, 5), new Pawn(Color.WHITE));
		board.put(new Position(6, 6), new Pawn(Color.WHITE));
		board.put(new Position(6, 7), new Pawn(Color.WHITE));
		
		board.put(new Position(7, 0), new Rook(Color.WHITE));
		board.put(new Position(7, 1), new Knight(Color.WHITE));
		board.put(new Position(7, 2), new Bishop(Color.WHITE));
		board.put(new Position(7, 3), new King(Color.WHITE));
		board.put(new Position(7, 4), new Queen(Color.WHITE));
		board.put(new Position(7, 5), new Bishop(Color.WHITE));
		board.put(new Position(7, 6), new Knight(Color.WHITE));
		board.put(new Position(7, 7), new Rook(Color.WHITE));
	}
	
//	public Piece GetPiece(Position p){
//		return board.get(p);
//	}
	
	public Map<Position, List<Move>> GenerateMoves(Color color) {
		Map<Position, List<Move>> moves = new HashMap<Position, List<Move>>();
		
		for(Position p : board.keySet()){
			Piece piece = board.get(p);
			if(piece != null && piece.color == color) {
				moves.put(p,  piece.PossibleMoves(p));
			}
		}
		
		return moves;
	}
	
	public void ApplyMove(Move move) {
		Piece fPiece = board.get(move.from);
		Piece tPiece = board.get(move.to);
		
		board.remove(move.from);
		//if(board.containsKey(move.to))
		//	board.replace(move.to, fPiece);
		//else
		//	board.put(move.to, fPiece);
		board.put(move.to, fPiece);
		
		if(tPiece != null && tPiece.name.equals("King")) {
			if(tPiece.color == Color.BLACK)
				state = State.WHITEWIN;
			else
				state = State.BLACKWIN;
		}
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
					System.out.print(boardArray[i][j].name.charAt(0) + " ");
			}
			System.out.println();
		}
	}
}
