package chessgame.Classes;

import chessgame.Interfaces.IPlayer;

public class Player implements IPlayer {
	int playerID;
	String playerName;
	Piece.Color playerColor;
	
	public Player(Piece.Color color){
		playerColor = color;
	}
	
	@Override
	public boolean MovePiece(String initialPosition, String destPosition) {
		// TODO Auto-generated method stub
		return false;
	}

}
