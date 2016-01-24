package chessgame.Interfaces;

public interface IGameServer {
	public boolean SendMove(int gameID, int playerID, String initialPosition, String destPosition);
	public boolean CloseGame(int gameID);
}
