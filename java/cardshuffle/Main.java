package com.analyticobjects.cardshuffle;

/**
 * Card shuffler testing.
 * 
 * @author Joel Bondurant
 * @since 2013.10.10
 */
public class Main {
	
	public static void main(String[] args) {
		Deck deck = new Deck();
		JTimer timer = new JTimer();
		int repeats = 1_000_000;
		timer.tic();
		deck.defaultCollectionsShuffle(repeats);
		timer.toc("defaultCollectionsShuffle");
		timer.tic();
		deck.collectionsShuffleRand(repeats);
		timer.toc("collectionsShuffleRand");
		timer.tic();
		deck.collectionsShuffleSecRand(repeats);
		timer.toc("collectionsShuffleSecRand");
		timer.tic();
		deck.joelShuffleV1(repeats);
		timer.toc("joelShuffleV1");
		timer.tic();
		deck.joelShuffleV2(repeats);
		timer.toc("joelShuffleV2");
	}
	
	
}
