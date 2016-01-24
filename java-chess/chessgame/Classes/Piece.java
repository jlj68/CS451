package chessgame.Classes;

import java.util.ArrayList;

public abstract class Piece {
	public String pieceName;
	public Color pieceColor;
	
	public enum Color{ BLACK, WHITE };
	
	public Piece(String name, Color c){
		pieceName = name;
		pieceColor = c;
	}
	
	public abstract ArrayList<Position> PossibleMoves(Position position);
}
