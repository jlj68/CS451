package chessgame.Classes;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Scanner;

import chessgame.Interfaces.IGame;
import chessgame.Interfaces.IPlayer;

public class Player implements IPlayer {
	int playerID;
	String playerName;
	Color playerColor;
	
	public Player(Color color){
		playerColor = color;
	}
	
	@Override
	public Move GetMove(IGame game) {
		Map<Position, List<Move>> moves = game.GenerateMoves();
		List<Move> lMoves = new ArrayList();
		
		int i = 1;
		for(Position p : moves.keySet()){
			List<Move> temp = moves.get(p);
			for(Move m : temp) {
				lMoves.add(m);
				System.out.println(Integer.toString(i) + ". " + m.toString());
				i++;
			}
		}
		
		System.out.println("Choose Move => ");
		Scanner sc = new Scanner(System.in);
		int choice = sc.nextInt()-1;

		return lMoves.get(choice);
	}

}
