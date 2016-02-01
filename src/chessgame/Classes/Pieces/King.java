package chessgame.Classes.Pieces;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

import chessgame.Classes.ChessBoard;
import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class King extends Piece{

	public King(Color color) {
		super("King", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position, ChessBoard board) {
		Position[] positions = {
				new Position(position.row+1, position.column),
				new Position(position.row-1, position.column),
				new Position(position.row, position.column+1),
				new Position(position.row, position.column-1),
				new Position(position.row+1, position.column+1),
				new Position(position.row-1, position.column+1),
				new Position(position.row+1, position.column-1),
				new Position(position.row-1, position.column-1)
		};
		
		ArrayList<Position> destination = new ArrayList<Position>();
		for(int i=0; i<positions.length; i++) {
			Piece piece = board.GetPiece(positions[i]);
			if(piece == null)
				destination.add(positions[i]);
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
