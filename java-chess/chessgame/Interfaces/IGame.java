package chessgame.Interfaces;

import java.util.List;
import java.util.Map;

import chessgame.Classes.Move;
import chessgame.Classes.Position;

public interface IGame {
	public void DisplayGame();
	public boolean IsGameOver();
	public Map<Position, List<Move>> GenerateMoves();
	public void ApplyMove(Move move);
}