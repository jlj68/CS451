package chessgame.Classes;

import java.util.List;
import java.util.Map;

import chessgame.Interfaces.IGame;

public class Game implements IGame {
	
	private ChessBoard b = new ChessBoard();
	public Color current = Color.BLACK;
	
	
	public ChessBoard GetChessBoard() {
		return b;
	}
	
	public void DisplayGame() {
		String sCurrent = (current == Color.BLACK ? "BLACK" : "WHITE");
		System.out.println("Current Player: " + sCurrent);
		b.PrintBoard();
	}
	
	public boolean IsGameOver() {
		return (b.state != State.MATCH) ? true : false;
	}
	
	public State GetResult() {
		return b.state;
	}
	
	public Map<Position, List<Move>> GenerateMoves() {
		return b.GenerateMoves(current);
	}
	
	public void ApplyMove(Move move) {
		b.ApplyMove(move);
		current = (current == Color.BLACK) ? Color.WHITE : Color.BLACK;
	}
}
