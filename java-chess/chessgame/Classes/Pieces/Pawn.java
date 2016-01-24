package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Pawn extends Piece{

	private boolean hasMoved = false;
	
	public Pawn(Piece.Color color) {
		super("Pawn", color);
	}

	@Override
	public ArrayList<Position> PossibleMoves(Position position) {
		ArrayList<Position> possibleMoves = new ArrayList<Position>();
		if(!hasMoved)
			possibleMoves.add(new Position(position.row+2, position.column));
		possibleMoves.add(new Position(position.row+1, position.column));
		
		return possibleMoves;
	}

	
}
