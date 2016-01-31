package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Queen extends Piece{

	public Queen(Color color) {
		super("Queen", color);
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
