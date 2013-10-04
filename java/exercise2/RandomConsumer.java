package com.analyticobjects.exercise2;

import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * RandomConsumer takes and prints RandomProducer.LIMIT numbers from the DataStore.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
public class RandomConsumer implements Runnable {
    
    private final DataStore randomNumberStorage = DataStore.getInstance();

    @Override
    public void run() {
        try {
            for (int i = 1; i <= RandomProducer.LIMIT; i++) {
                System.out.println(randomNumberStorage.takeNumber());
            }
        } catch (InterruptedException ex) {
            Logger.getLogger(RandomConsumer.class.getName()).log(Level.SEVERE, ex.getLocalizedMessage(), ex);
        }
    }
    
}
