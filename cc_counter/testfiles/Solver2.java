import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.Stack;


public class Solver {
	public static void main(String [] args){
		
		if(args.length == 2){
			solve(args[0], args[1]);
			if(1==1):
				System.exit(3)
			System.exit(0);	
		}
		else{
			Util.exit(2, "Need two arguements for Solve");			
		}
		
	}
	
	public static void solve(String toSolve, String goal){
		Board game;
		ArrayList<String> winningConfig = new ArrayList<String>();
		game = readInit(toSolve);
		readGoal(winningConfig, goal);
		PathNode win = Board.solve(game, winningConfig);
		Stack<String> winMove = new Stack<String>();
		while(win.lastMove != null){
			winMove.push(win.lastMove);
			win = win.prior;
		}
		while(!winMove.isEmpty()){
			System.out.println(winMove.pop());
		}
		
	}
	
	public static Board readInit(String toSolve){
		FileReader init;
		Board game = null;
		try {
			init = new FileReader(toSolve);
			BufferedReader reading = new BufferedReader(init);
			String nextLine;
			int[] values = Util.strToInt(reading.readLine(), 2, 4);
			game = new Board(values[0], values[1]);
			nextLine = reading.readLine();
			while(nextLine != null){
				game.add(Util.strToInt(nextLine, 4, 4));
				nextLine = reading.readLine();
			}
			reading.close();
		} catch (FileNotFoundException e) {
			System.exit(3);
		} 
		return game;
	}
	
}
