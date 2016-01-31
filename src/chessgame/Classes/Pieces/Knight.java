package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Knight extends Piece{

	public Knight(Color color) {
		super("Knight", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position) {
		ArrayList<Position> destination = new ArrayList<Position>();
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		
		destination.add(new Position(2, 1));
		destination.add(new Position(2, -1));
		destination.add(new Position(-2, 1));
		destination.add(new Position(-2, -1));
		destination.add(new Position(1, 2));
		destination.add(new Position(1, -2));
		destination.add(new Position(-1, 2));
		destination.add(new Position(-1, -2));
		
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

}
