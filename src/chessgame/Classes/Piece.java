package chessgame.Classes;

import java.util.ArrayList;

public abstract class Piece {
	public String name;
	public Color color;
	
	public Piece(String aName, Color aColor){
		name = aName;
		color = aColor;
	}
	
	public abstract ArrayList<Move> PossibleMoves(Position position);
}
