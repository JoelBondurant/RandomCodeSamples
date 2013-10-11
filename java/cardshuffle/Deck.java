package com.analyticobjects.cardshuffle;

import com.analyticobjects.cardshuffle.Card.Rank;
import com.analyticobjects.cardshuffle.Card.Suit;
import java.security.SecureRandom;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Random;

public class Deck {
	
	private final List<Card> cards;
	private SecureRandom srand;
	private Random rand;
	
	public Deck() {
		this.srand = new SecureRandom();
		this.rand = new Random(this.srand.nextLong());
		this.cards = new ArrayList<>(52);
		for (Suit suit : Card.Suit.values()) {
			for (Rank rank : Card.Rank.values()) {
				this.cards.add(new Card(suit, rank));
			}
		}
	}
	
	public void printDeck() {
		for (Card card : this.cards) {
			System.out.println(card);
		}
	}
	
	public void defaultCollectionsShuffle(int repeats) {
		for (int i = 0; i < repeats; i++) {
			defaultCollectionsShuffle();
		}
	}
	
	public void defaultCollectionsShuffle() {
		Collections.shuffle(cards);
	}
	
	public void collectionsShuffleRand(int repeats) {
		for (int i = 0; i < repeats; i++) {
			collectionsShuffleRand();
		}
	}
	
	public void collectionsShuffleRand() {
		Collections.shuffle(cards, rand);
	}
	
	public void collectionsShuffleSecRand(int repeats) {
		for (int i = 0; i < repeats; i++) {
			collectionsShuffleSecRand();
		}
	}
	
	public void collectionsShuffleSecRand() {
		Collections.shuffle(cards, srand);
	}
	
	public void joelShuffleV1(int repeats) {
		for (int i = 0; i < repeats; i++) {
			joelShuffleV1();
		}
	}
	
	public void joelShuffleV1() {
		int deckSize = cards.size();
		List<CardSort> cardSorts = new ArrayList<>(deckSize);
		for (int i = 0; i < deckSize; i++) {
			cardSorts.add(new CardSort(i, rand.nextInt()));
		}
		Collections.sort(cardSorts);
		int i = 0;
		for (CardSort cardSort : cardSorts) {
			Card thatCard = this.cards.get(cardSort.originalIndex);
			Card thisCard = this.cards.get(i);
			this.cards.set(i, thatCard);
			this.cards.set(cardSort.originalIndex, thisCard);
			i++;
		}
	}
	
	public void joelShuffleV2(int repeats) {
		for (int i = 0; i < repeats; i++) {
			joelShuffleV2();
		}
	}
	
	public void joelShuffleV2() {
		Card cardHolder;
		Card randomCard;
		int randInt;
		for (int i = this.cards.size() -1; i > 0; i--) {
			cardHolder = this.cards.get(i);
			randInt = rand.nextInt(i);
			randomCard = this.cards.get(randInt);
			this.cards.set(i, randomCard);
			this.cards.set(randInt, cardHolder);
		}
	}
	
	private class CardSort implements Comparable {
		
		int originalIndex;
		int randomizer;
		
		CardSort(int originalIndex, int randomizer) {
			this.originalIndex = originalIndex;
			this.randomizer = randomizer;
		}

		@Override
		public int compareTo(Object obj) {
			if (!(obj instanceof CardSort)) {
				return -1;
			}
			CardSort other = (CardSort) obj;
			if (this.originalIndex > other.originalIndex) {
				return 1;
			}
			return -1;
		}
	}
	
}
