package chessgame.Classes;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.google.gson.Gson;
import com.google.gson.JsonObject;

import chessgame.Classes.Pieces.*;

public class ChessBoard {	
	public Piece[][] board;
	public State state = State.MATCH;
	
	public ChessBoard() {
		board = new Piece[8][];
		for(int i=0; i<board.length; i++) {
			board[i] = new Piece[8];
			for(int j=0; j<board[i].length; j++) {
				board[i][j] = null;
			}
		}

		board[0][0] = new Rook(Color.BLACK);
		board[0][1] = new Knight(Color.BLACK);
		board[0][2] = new Bishop(Color.BLACK);
		board[0][3] = new Queen(Color.BLACK);
		board[0][4] = new King(Color.BLACK);
		board[0][5] = new Bishop(Color.BLACK);
		board[0][6] = new Knight(Color.BLACK);
		board[0][7] = new Rook(Color.BLACK);
		
		board[1][0] = new Pawn(Color.BLACK);
		board[1][1] = new Pawn(Color.BLACK);
		board[1][2] = new Pawn(Color.BLACK);
		board[1][3] = new Pawn(Color.BLACK);
		board[1][4] = new Pawn(Color.BLACK);
		board[1][5] = new Pawn(Color.BLACK);
		board[1][6] = new Pawn(Color.BLACK);
		board[1][7] = new Pawn(Color.BLACK);
		
		
		board[6][0] = new Pawn(Color.WHITE);
		board[6][1] = new Pawn(Color.WHITE);
		board[6][2] = new Pawn(Color.WHITE);
		board[6][3] = new Pawn(Color.WHITE);
		board[6][4] = new Pawn(Color.WHITE);
		board[6][5] = new Pawn(Color.WHITE);
		board[6][6] = new Pawn(Color.WHITE);
		board[6][7] = new Pawn(Color.WHITE);
		
		board[7][0] = new Rook(Color.WHITE);
		board[7][1] = new Knight(Color.WHITE);
		board[7][2] = new Bishop(Color.WHITE);
		board[7][3] = new King(Color.WHITE);
		board[7][4] = new Queen(Color.WHITE);
		board[7][5] = new Bishop(Color.WHITE);
		board[7][6] = new Knight(Color.WHITE);
		board[7][7] = new Rook(Color.WHITE);
	}
	
	public Piece GetPiece(Position p){
		if(p.row<8 && p.row>-1 && p.column<8 && p.column>-1)
			return board[p.row][p.column];
		return null;
	}
	
	public Map<Position, List<Move>> GenerateMoves(Color color) {
		Map<Position, List<Move>> moves = new HashMap<Position, List<Move>>();
		
		for(int i=0; i<8; i++) {
			for(int j=0; j<8; j++) {
				Position p = new Position(i, j);
				Piece piece = board[i][j];
				if(piece != null && piece.color == color) {
					moves.put(p, piece.PossibleMoves(p, this));
				}
			}
		}
		
		return moves;
	}
	
	public void ApplyMove(Move move) {
		Piece fPiece = board[move.from.row][move.from.column];
		Piece tPiece = board[move.to.row][move.to.column];
		
		board[move.from.row][move.from.column] = null;
		board[move.to.row][move.to.column] = fPiece;
		
		fPiece.hasMoved = true;
		
		if(tPiece != null && tPiece.name.equals("King")) {
			if(tPiece.color == Color.BLACK)
				state = State.WHITEWIN;
			else
				state = State.BLACKWIN;
		}
	}
	
	public void PrintBoard(){
		System.out.println("  0 1 2 3 4 5 6 7");
		for(int i = 0; i < 8; i++){
			System.out.print(i+" ");
			for(int j = 0; j < 8; j++){
				if(board[i][j] == null)
					System.out.print("- ");
				else
					System.out.print(board[i][j].name.charAt(0) + " ");
			}
			System.out.println();
		}
	}
	
	public String getBoardJson(){
		Gson gson = new Gson();
		return gson.toJson(board);
	}
}
