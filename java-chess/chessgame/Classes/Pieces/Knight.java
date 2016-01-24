package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Knight extends Piece{

	public Knight(Piece.Color color) {
		super("Knight", color);
	}

	@Override
	public ArrayList<Position> PossibleMoves(Position position) {
		ArrayList<Position> possiblePositions = new ArrayList<Position>();
		
		possiblePositions.add(new Position(2, 1));
		possiblePositions.add(new Position(2, -1));
		possiblePositions.add(new Position(-2, 1));
		possiblePositions.add(new Position(-2, -1));
		possiblePositions.add(new Position(1, 2));
		possiblePositions.add(new Position(1, -2));
		possiblePositions.add(new Position(-1, 2));
		possiblePositions.add(new Position(-1, -2));
		
		for(Position p : possiblePositions)
			if(p.row > 7 || p.row < 0 || p.column > 7 || p.column > 0)
				possiblePositions.remove(p);
		
		return possiblePositions;
	}

}
