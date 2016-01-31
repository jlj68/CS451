package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Pawn extends Piece{

	private boolean hasMoved = false;
	
	public Pawn(Color color) {
		super("Pawn", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position) {
		ArrayList<Position> destination = new ArrayList<Position>();
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		
		if(!hasMoved)
			destination.add(new Position(position.row+2, position.column));
		destination.add(new Position(position.row+1, position.column));
		
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

	
}
