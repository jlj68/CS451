package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class King extends Piece{

	public King(Piece.Color color) {
		super("King", color);
	}

	@Override
	public ArrayList<Position> PossibleMoves(Position position) {
		ArrayList<Position> possiblePositions = new ArrayList<Position>();
		
		possiblePositions.add(new Position(position.row+1, position.column));
		possiblePositions.add(new Position(position.row-1, position.column));
		possiblePositions.add(new Position(position.row, position.column+1));
		possiblePositions.add(new Position(position.row, position.column-1));
		possiblePositions.add(new Position(position.row+1, position.column+1));
		possiblePositions.add(new Position(position.row-1, position.column+1));
		possiblePositions.add(new Position(position.row+1, position.column-1));
		possiblePositions.add(new Position(position.row-1, position.column-1));
		
		for(Position p : possiblePositions)
			if(p.row > 7 || p.row < 0 || p.column > 7 || p.column > 0)
				possiblePositions.remove(p);
		
		return possiblePositions;
	}
	
}
