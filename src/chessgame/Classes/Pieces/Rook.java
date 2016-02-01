package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.ChessBoard;
import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Rook extends Piece{

	public Rook(Color color) {
		super("Rook", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position, ChessBoard board) {
		Position[] delta = {
				new Position(1, 0),
				new Position(-1, 0),
				new Position(0, 1),
				new Position(0, -1)
		};
		
		ArrayList<Position> destination = super.GetFilterPositions(board, position, delta);
		
		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

	
}
