package chessgame.Classes;

import chessgame.Interfaces.IGame;

public class Game implements IGame{
	
	private static ChessBoard b;
	
	public static void main(String[] args){
		b = new ChessBoard();
		b.PrintBoard();
		
		Player player1 = new Player(Piece.Color.WHITE);
		Player player2 = new Player(Piece.Color.BLACK);
		
		
	}
	
	@Override
	public boolean MakeMove(Player mover, Position initialPosition, Position destPosition) {
		if(mover.playerColor == b.GetPiece(initialPosition).pieceColor && b.GetPiece(initialPosition).PossibleMoves(initialPosition).contains(destPosition))
			return true;
		return false;
	}

	@Override
	public boolean CheckWin() {
		// TODO Auto-generated method stub
		return false;
	}
	
}
