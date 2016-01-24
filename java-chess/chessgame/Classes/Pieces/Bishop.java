package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Bishop extends Piece{

	public Bishop(Piece.Color color) {
		super("Bishop", color);
	}

	@Override
	public ArrayList<Position> PossibleMoves(Position position) {
		ArrayList<Position> possiblePositions = new ArrayList<Position>();
		
		for(int i = 1; i < 8; i++){
			possiblePositions.add(new Position(position.row+i, position.column+i));
			possiblePositions.add(new Position(position.row+i, position.column-i));
			possiblePositions.add(new Position(position.row-i, position.column+i));
			possiblePositions.add(new Position(position.row-i, position.column-i));
		}
		
		for(Position p : possiblePositions)
			if(p.row > 7 || p.row < 0 || p.column > 7 || p.column > 0)
				possiblePositions.remove(p);
		
		return possiblePositions;
	}

}
