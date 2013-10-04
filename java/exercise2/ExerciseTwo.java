package com.analyticobjects.exercise2;

/**
 * Exercise 2.
 * 
 * Please write a program that does the following:
 * 1. A Producer class produces a randomly generated number
 * 2. The Producer class stores this number into a DataStore class
 * 3. A consumer class consumes a number from the DataStore class and displays it to
 * System.out.
 * The program should run until the Producer produces 100 numbers. The Producer and
 * Consumer should be running in parallel, in other words, the Consumer should be able to
 * consume numbers before the Producer is done producing all 100 numbers.
 * 
 * @author Joel Bondurant
 * @since 2013.10.04
 */
public class ExerciseTwo {
    
    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        new Thread(new RandomProducer()).start();
        new Thread(new RandomConsumer()).start();
    }
}
