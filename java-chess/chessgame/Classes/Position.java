package chessgame.Classes;

public class Position {
	public int row;
	public int column;
	
	public Position(int r, int c){
		row = r;
		column = c;
	}
	
	public String toString() {
		return "(" + Integer.toString(row) + ", " + Integer.toString(column) + ")";
	}
}
