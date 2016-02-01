package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.ChessBoard;
import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Knight extends Piece{

	public Knight(Color color) {
		super("Knight", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position, ChessBoard board) {
		Position[] positions = {
				new Position(position.row+2, position.column+1),
				new Position(position.row+2, position.column-1),
				new Position(position.row-2, position.column+1),
				new Position(position.row-2, position.column-1),
				new Position(position.row+1, position.column+2),
				new Position(position.row-1, position.column+2),
				new Position(position.row+1, position.column-2),
				new Position(position.row-1, position.column-2)
		};
		
		ArrayList<Position> destination = new ArrayList<Position>();
		for(int i=0; i<positions.length; i++) {
			Piece piece = board.GetPiece(positions[i]);
			if(piece == null) {
				destination.add(positions[i]);
			}
			else if(piece.color != color) {
				destination.add(positions[i]);
			}
		}
		
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}
}
