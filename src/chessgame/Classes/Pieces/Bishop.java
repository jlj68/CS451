package chessgame.Classes.Pieces;

import java.util.ArrayList;

import chessgame.Classes.ChessBoard;
import chessgame.Classes.Color;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;
import chessgame.Classes.Move;

public class Bishop extends Piece{

	public Bishop(Color color) {
		super("Bishop", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position, ChessBoard board) {
		Position[] delta = {
				new Position(1, 1),
				new Position(1, -1),
				new Position(-1, 1),
				new Position(-1, -1)
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
