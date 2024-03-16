import java.util.*;

public class RNG {
	
	private static Random rand = null; 
	private int weights[];
	private int total_weight = 0;
	
	public RNG() {
		if(rand == null) {
			rand = new Random(System.nanoTime());
		}
	}
	
	public RNG(int weights[]) {
		if(rand == null) {
			rand = new Random(System.nanoTime());
		}
		
		this.weights = weights;
		
		for(int i : weights) {
			total_weight += i;
		}
	}
	
	int getRand(int range) {
		return rand.nextInt(range);
	}
	
	int getRandIndex() {
		int range = rand.nextInt(total_weight);
		
		for(int index = 0; index < weights.length; index++) {
			
			if(range < weights[index])
				return index;
			
			range -= weights[index];
		}
		
		System.out.println("Error in getRandIndex().");
		return -1;
	}
	
	void getWeights() {
		for(int i = 0; i < weights.length; i++) {
			System.out.print(weights[i] + " ");
		}
		System.out.println();
	}
}
