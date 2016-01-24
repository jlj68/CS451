package chessgame.Interfaces;

import chessgame.Classes.Player;
import chessgame.Classes.Position;

public interface IGame {
	public boolean MakeMove(Player mover, Position initialPosition, Position destPosition);
	public boolean CheckWin();
}
