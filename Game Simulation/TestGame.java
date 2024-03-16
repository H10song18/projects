
public class TestGame {

	public static void main(String[] args) {
		
		long sims = 1000000000L;
		
		Game game = new Game(1);
		game.analyzeReel(false);
		game.analyzeReel(true);
		
		for(long i = 0; i < sims; i++) {
			game.playGame();
			
			if((i+1) % Math.max(1, (sims / 100)) == 0)
			{
				game.printStats();
				System.out.println();
			}
		}
		
		game.printStats();
		game.printStats("Simulation Results.txt");
	}

}
