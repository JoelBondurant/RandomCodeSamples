package com.analyticobjects.exercise3;

import java.util.HashSet;
import java.util.Set;


/**
 * Exercise 3.
 * 
 * An anagram is a type of word play, the result of rearranging the letters of a word or phrase to
 * produce a new word or phrase, using all the original letters exactly once. In other words, “cat”
 * and “act” would be considered anagrams since they share the exact same letters just in
 * different order. Whereas “act” would not be an anagram of “acts” because “acts” has an “s” and
 * “act” does not.
 * 
 * Taking the the list of words below, output all word pairs that are “anagrams” of each other.
 * Please display each anagram word pair to System.out in format like this:
 * 
 * wordX wordY
 * wordA wordB
 * 
 * Word List:
 * vase bat gods latte name apres spit joke ham dog act tale parse pits asper tab table mane late
 * god cat table save spare
 * 
 * @author Joel Bondurant
 * @since 2013.10.04
 */
public class ExerciseThree {
    
    private static final String[] wordArray = {"vase","bat","gods","latte","name","apres","spit","joke",
        "ham","dog","act","tale","parse","pits","asper","tab","table","mane","late","god","cat","table",
        "save","spare"};
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        for (String word : wordArray) {
            anagrammer(word);
        }
    }
    
    private static void anagram(Set<String> accumulator, String wordInput, String wordOutput) {
        if (wordInput.length() == 0) {
            accumulator.add(wordOutput);
        }
        for (int i = 0; i < wordInput.length(); i++) {
            anagram(accumulator, wordInput.substring(0, i) + wordInput.substring(i + 1, wordInput.length()), wordInput.charAt(i) + wordOutput);
        }
    }
    
    private static void anagrammer(String word) {
        // A full implementation might check the words against a dictionary.
        Set<String> anagrams = new HashSet<>();
        anagram(anagrams, word, "");
        for (String anagram : anagrams) {
            if (!anagram.equals(word)) { // remove if same word anagram is needed.
                System.out.println(word + ", " + anagram);
            }
        }
    }
}
