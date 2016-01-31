package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Color;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;
import chessgame.Classes.Move;

public class Bishop extends Piece{

	public Bishop(Color color) {
		super("Bishop", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position) {
		ArrayList<Position> destination = new ArrayList<Position>();
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		
		for(int i = 1; i < 8; i++){
			destination.add(new Position(position.row+i, position.column+i));
			destination.add(new Position(position.row+i, position.column-i));
			destination.add(new Position(position.row-i, position.column+i));
			destination.add(new Position(position.row-i, position.column-i));
		}
		
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

}
