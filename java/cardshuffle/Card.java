package com.cloudwords.cardshuffle;

public class Card {
	
	public final Suit suit;
	public final Rank rank;
	
	public Card(Suit suit, Rank rank) {
		this.suit = suit;
		this.rank = rank;
	}
	
	@Override
	public String toString() {
		return this.rank.name() + " of " + this.suit.name() + "s";
	}
	
	public enum Suit {Spade, Diamond, Club, Heart};
	
	public enum Rank {Two, Three, Four, Five, Six, Seven, Eight, Nine, Ten, Jack, Queen, King, Ace};
	
}
