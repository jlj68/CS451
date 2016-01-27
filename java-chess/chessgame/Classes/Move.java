package chessgame.Classes;

public class Move {
	public Position from;
	public Position to;
	
	public Move(Position aFrom, Position aTo) {
		from = aFrom;
		to = aTo;
	}
	
	public String toString() {
		return from.toString() + " -> " + to.toString();
	}
}
