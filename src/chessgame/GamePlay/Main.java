package chessgame.GamePlay;

import chessgame.Classes.Color;
import chessgame.Classes.Game;
import chessgame.Classes.Player;
import chessgame.Classes.Move;

public class Main {
	public static void main(String[] args){
		Game game = new Game();
		
		Player player1 = new Player(Color.WHITE);
		Player player2 = new Player(Color.BLACK);
		
		while(!game.IsGameOver()) {
			game.DisplayGame();
			System.out.println();
			Move move = (game.current == Color.BLACK) ? player2.GetMove(game): player1.GetMove(game);
			game.ApplyMove(move);
		}
		
		System.out.println(game.GetResult().toString());
		
	}
}
