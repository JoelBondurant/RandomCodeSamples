package com.cloudwords.cardshuffle;

public class JTimer {
	
	private long tic;
	private long toc;
	
	public JTimer() {
		this.tic = 0L;
		this.toc = 0L;
	}
	
	public void tic() {
		this.tic = System.nanoTime();
	}
	
	public String toc() {
		this.toc = System.nanoTime();
		return Long.toString((toc - tic)/1_000_000L);
	}
	
	public void toc(String label) {
		System.out.println("time:<"+label+"> "+toc()+" ms.");
	}
	
}
