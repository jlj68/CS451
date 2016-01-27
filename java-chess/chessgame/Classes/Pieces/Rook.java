package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Rook extends Piece{

	public Rook(Color color) {
		super("Rook", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position) {
		ArrayList<Position> destination = new ArrayList<Position>();
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		
		for(int i = 0; i < 7; i++)
			if(i != position.column)
				destination.add(new Position(position.row, i));
		
		for(int i = 0; i < 7; i++)
			if(i != position.row)
				destination.add(new Position(i, position.column));
		
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

}
