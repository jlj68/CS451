package chessgame.Classes;

import java.util.ArrayList;

public abstract class Piece {
	public boolean hasMoved = false;
	public String name;
	public Color color;
	
	public Piece(String aName, Color aColor){
		name = aName;
		color = aColor;
	}
	
	public abstract ArrayList<Move> PossibleMoves(Position position, ChessBoard board);
	
	protected ArrayList<Position> FilterPositions(ChessBoard board, Position current, Position delta) {
		ArrayList<Position> destination = new ArrayList<Position>();
		current = new Position(current.row+delta.row, current.column+delta.column);
		
		while(current.row < 8 && current.row > -1 && current.column < 8 && current.column > -1) {
			Piece piece = board.GetPiece(current);
			if(piece == null)
				destination.add(current);
			else if(piece.color != color) {
				destination.add(current);
				break;
			}
			else
				break;
			
			current = new Position(current.row+delta.row, current.column+delta.column);
		}
		return destination;
	}
	
	protected ArrayList<Position> GetFilterPositions(ChessBoard board, Position current, Position[] delta) {
		ArrayList<Position> destination = new ArrayList<Position>();
		
		for(int i=0; i<delta.length; i++) {
			ArrayList<Position> path = FilterPositions(board, current, delta[i]);
			for(int j=0; j<path.size(); j++)
				destination.add(path.get(j));
		}
		return destination;
	}
	
	public String toString(){
		return "" + color.toString().charAt(0) + name.charAt(0);
	}
}
