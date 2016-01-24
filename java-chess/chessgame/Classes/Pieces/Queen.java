package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Queen extends Piece{

	public Queen(Piece.Color color) {
		super("Queen", color);
	}

	@Override
	public ArrayList<Position> PossibleMoves(Position position) {
		ArrayList<Position> possiblePositions = new ArrayList<Position>();
		
		for(int i = 0; i < 7; i++)
			if(i != position.column)
				possiblePositions.add(new Position(position.row, i));
		
		for(int i = 0; i < 7; i++)
			if(i != position.row)
				possiblePositions.add(new Position(i, position.column));
		
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
