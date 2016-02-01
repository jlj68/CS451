package chessgame.Classes.Pieces;

import java.util.List;
import java.util.ArrayList;

import chessgame.Classes.ChessBoard;
import chessgame.Classes.Color;
import chessgame.Classes.Move;
import chessgame.Classes.Piece;
import chessgame.Classes.Position;

public class Pawn extends Piece{

	public Pawn(Color color) {
		super("Pawn", color);
	}

	@Override
	public ArrayList<Move> PossibleMoves(Position position, ChessBoard board) {
		ArrayList<Position> destination = new ArrayList<Position>();
		int direction = color==Color.BLACK ? 1 : -1;
		
		Position[] positions = {
				new Position(position.row+direction, position.column+1),
				new Position(position.row+direction, position.column-1)
		};
		
		for(int i=0; i<positions.length; i++) {
			Piece piece = board.GetPiece(positions[i]);
			if(piece != null && piece.color != color)
				destination.add(positions[i]);
		}
		
		
		List<Position> po = new ArrayList<Position>();
		if(!hasMoved)
			po.add(new Position(position.row+2*direction, position.column));
		po.add(new Position(position.row+direction, position.column));
		
		for(int i=0; i<po.size(); i++) {
			Piece piece = board.GetPiece(po.get(i));
			if(piece == null)
				destination.add(po.get(i));
		}

		ArrayList<Move> possiblePositions = new ArrayList<Move>();
		for(Position p : destination) {
			if(!(p.row > 7 || p.row < 0 || p.column > 7 || p.column < 0))
				possiblePositions.add(new Move(position, p));
		}
		
		return possiblePositions;
	}

	
}
