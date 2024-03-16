import java.lang.Math; 
import java.util.*;
import java.io.*;

public class GameStats {
	private long
		games_played = 0,
		total_in = 0,
		total_in2 = 0,
		total_out = 0,
		total_out2 = 0;
	
	private double
		rtp = 0.0,
		variance = 0.0,
		std_dev = 0.0;
	
	private Map<Integer, Long> pay_hits;
	private Map<String, Long> award_hits;
	
	public GameStats() {
		pay_hits = new HashMap<Integer, Long>();
		award_hits = new HashMap<String, Long>();
	}
	
	void addWin(int wager, int win) {
		games_played++;
		total_in += wager;
		total_in2 += wager * wager;
		total_out += win;
		total_out2 += win * win;
		
		rtp = (double) total_out / (double) total_in;
		variance = ((double)total_out2 / (double)total_in2) - (rtp * rtp);
		std_dev = Math.sqrt(variance);
	}
	
	void addAward(String symbol_name, int count, int pay) {
		pay_hits.merge(pay, 1L, Long::sum);
		String award = symbol_name + "\t" + Integer.toString(count) + "\t" + Integer.toString(pay);
		award_hits.merge(award, 1L, Long::sum);
	}
	
	void getStats() {
		System.out.println("Games Played:\t" + games_played);
		System.out.println("RTP:\t" + rtp);
		System.out.println("SD:\t" + std_dev);
	}
	
	void printStats(String filename) {
		try {
			FileWriter fw = new FileWriter(filename, false);
			fw.write("Games Played:\t" + games_played + "\n");
			fw.write("Total In:\t" + total_in + "\n");
			fw.write("Total Out:\t" + total_out + "\n");
			fw.write("Total In2:\t" + total_in2 + "\n");
			fw.write("Total Out2:\t" + total_out2 + "\n");
			fw.write("\n");
			
			printOdds(fw);
			
			fw.close();
		}
		catch (Exception e) {
			System.out.println("Error in creating " + filename + ".");
		}
	}
	
	void printOdds(FileWriter fw) throws IOException {
		TreeMap<Integer, Long> tm1 = new TreeMap<Integer, Long>();
		tm1.putAll(pay_hits);
		
		fw.write("Pay:\t" + "Hits:\n");
		for(Map.Entry<Integer, Long> it : tm1.entrySet()) {
			fw.write(it.getKey() + "\t" + it.getValue() + "\n");
		}
		
		fw.write("\n");
		
		TreeMap<String, Long> tm2 = new TreeMap<String, Long>();
		tm2.putAll(award_hits);
		
		fw.write("Symbol:\t" + "Count:\t" + "Pay:\t" + "Hits:\n");
		for(Map.Entry<String, Long> it : tm2.entrySet()) {
			fw.write(it.getKey() + "\t" + it.getValue() + "\n");
		}
	}
	
	void clear() {
		games_played = 0;
		total_in = 0;
		total_in2 = 0;
		total_out = 0;
		total_out2 = 0;
		
		rtp = 0.0;
		variance = 0.0;
		std_dev = 0.0;
		
		pay_hits.clear();
		award_hits.clear();
	}
}
