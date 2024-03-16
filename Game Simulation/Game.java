
public class Game extends GameData {
	
	private int screen[][];
	private int reel_stops[];
	private int bet_multiplier;
	private int wager;
	
	private RNG rand;
	private RNG scatter_dist;
	
	GameStats stats;
	
	public Game(int bm) {
		rand = new RNG();
		screen = new int[REEL_SIZE][ROW_SIZE];
		reel_stops = new int[REEL_SIZE];
		bet_multiplier = bm;
		wager = BASE_WAGER * bet_multiplier;
		
		scatter_dist = new RNG(SCATTER_DIST);
		
		stats = new GameStats();
	}
	
	private void spinReels() {
		for(int reel = 0; reel < REEL_SIZE; reel++) {
			reel_stops[reel] = rand.getRand(REELS[reel].length);
		}
	}
	
	private void setScreen() {
		for(int reel = 0; reel < REEL_SIZE; reel++) {
			for(int row = 0; row < ROW_SIZE; row++) {
				screen[reel][row] = REELS[reel][(reel_stops[reel] + REELS[reel].length + row) % REELS[reel].length];
			}
		}
	}
	
	private int[] lineEval(int line[]) {
		
		int count = 1;
		int wcount = 0;
		int curr_symbol = screen[0][line[0]];
		int symbol = curr_symbol;
		
		if(symbol >= BONUS)
			return new int[] {symbol, count};
		
		if(symbol == WILD)
			wcount++;
		
		for(int reel = 1; reel < REEL_SIZE; reel++) {
			
			curr_symbol = screen[reel][line[reel]];
			
			if(curr_symbol == WILD || curr_symbol == symbol) 
			{
				count++;
				if(curr_symbol == WILD)
					wcount++;
			}
			else if(symbol == WILD && curr_symbol < BONUS)
			{
				symbol = curr_symbol;
				count++;
			}
			else
			{
				break;
			}
		}
		
		if(wcount > 0 && PAYTABLE[WILD][wcount-1] > PAYTABLE[symbol][count-1])
		{
			symbol = WILD;
			count = wcount;
		}
		
		
		return new int[] {symbol, count};
	}
	
	private int getScreenPay() {
		int total_pays = 0;
		int line_result[] = new int[2]; 
		
		for(int i = 0; i < LINES.length; i++) {
			line_result = lineEval(LINES[i]);
			
			int symbol = line_result[0];
			int count = line_result[1];
			
			if(count > 1)
			{
				int temp_pay = PAYTABLE[symbol][count - 1];
				total_pays += temp_pay * bet_multiplier;
				
				if(temp_pay > 0)
					stats.addAward(SYMBOLS[symbol], count, temp_pay);
			}
		}
		
		return total_pays;
	}
	
	private int getScatterCount(int symbol) {
		int count = 0;
		
		for(int reel = 0; reel < REEL_SIZE; reel++) {
			for(int row = 0; row < ROW_SIZE; row++) {
				if(screen[reel][row] == symbol) {
					count++;
				}
			}
		}
		
		return count;
	}
	
	private void expandingWildsFeature() {
		for(int reel = 0; reel < REEL_SIZE; reel++) {
			for(int row = 0; row < ROW_SIZE; row++) {
				if(screen[reel][row] == WILD)
				{
					for(int r = 0; r < ROW_SIZE; r++) {
						screen[reel][r] = WILD;
					}
					break;
				}
			}
		}
	}
	
	private int bonusFeature() {
		int total_pays = 0;
		int fgs = FREE_GAMES;
		
		while(fgs > 0) {
			spinReels();
			setScreen();
			
			int bonus_count = getScatterCount(BONUS);
			int scatter_count = getScatterCount(SCATTER);
			
			if(bonus_count > 2)
			{
				total_pays += PAYTABLE[BONUS][bonus_count-1] * wager;
				fgs += FREE_GAMES;
				
				if(PAYTABLE[BONUS][bonus_count-1] > 0)
					stats.addAward(SYMBOLS[BONUS], bonus_count, PAYTABLE[BONUS][bonus_count-1] * BASE_WAGER);
			}
			
			if(scatter_count > 2)
			{
				int index = scatter_dist.getRandIndex();
				total_pays += SCATTER_PAYS[index] * bet_multiplier;
				
				stats.addAward(SYMBOLS[SCATTER], scatter_count, SCATTER_PAYS[index]);
			}
			
			expandingWildsFeature();
			
			total_pays += getScreenPay();
			
			fgs--;
		}
		
		return total_pays;
	}
	
	public void playGame() {
		int total_pays = 0;
		
		spinReels();
		setScreen();

		total_pays = getScreenPay();
		
		int bonus_count = getScatterCount(BONUS);
		int scatter_count = getScatterCount(SCATTER);
		
		if(bonus_count > 2)
		{
			total_pays += PAYTABLE[BONUS][bonus_count-1] * wager;
			total_pays += bonusFeature();
			
			if(PAYTABLE[BONUS][bonus_count-1] > 0)
				stats.addAward(SYMBOLS[BONUS], bonus_count, PAYTABLE[BONUS][bonus_count-1] * BASE_WAGER);
		}
		
		if(scatter_count > 2)
		{
			int index = scatter_dist.getRandIndex();
			total_pays += SCATTER_PAYS[index] * bet_multiplier;
			
			stats.addAward(SYMBOLS[SCATTER], scatter_count, SCATTER_PAYS[index]);
		}
		
		stats.addWin(wager, total_pays);
	}
	
	public void printStats() {
		stats.getStats();
	}
	
	public void printStats(String filename) {
		stats.printStats(filename);
	}
	
	public void analyzeReel(boolean is_bonus) {
		
		int total_pays;
		
		for(reel_stops[0] = 0; reel_stops[0] < REELS[0].length; reel_stops[0]++)
		for(reel_stops[1] = 0; reel_stops[1] < REELS[1].length; reel_stops[1]++)
		for(reel_stops[2] = 0; reel_stops[2] < REELS[2].length; reel_stops[2]++)
		for(reel_stops[3] = 0; reel_stops[3] < REELS[3].length; reel_stops[3]++)
		for(reel_stops[4] = 0; reel_stops[4] < REELS[4].length; reel_stops[4]++)
		{	
			total_pays = 0;
			
			setScreen();
			
			int bonus_count = getScatterCount(BONUS);
			int scatter_count = getScatterCount(SCATTER);
			
			if(bonus_count > 2)
			{
				total_pays += PAYTABLE[BONUS][bonus_count-1] * wager;
				
				if(PAYTABLE[BONUS][bonus_count-1] > 0)
					stats.addAward(SYMBOLS[BONUS], bonus_count, PAYTABLE[BONUS][bonus_count-1] * BASE_WAGER);
			}
			
			if(scatter_count > 2)
			{
				stats.addAward(SYMBOLS[SCATTER], scatter_count, 0);
			}
			
			if(is_bonus)
				expandingWildsFeature();
			
			total_pays += getScreenPay();
			
			stats.addWin(wager, total_pays);
		}	
		
		if(!is_bonus)
			stats.printStats("BaseStats.txt");
		else
			stats.printStats("BonusStats.txt");
		
		
		stats.clear();
		System.out.println("Complete.");
	}
	
	public void printScreen(int scr[][]) {
		for(int i = 0; i < ROW_SIZE; i++) {
			for(int j = 0; j < REEL_SIZE; j++) {
				System.out.print(scr[j][i] + " ");
			}
			System.out.println();
		}
	}
	
}
