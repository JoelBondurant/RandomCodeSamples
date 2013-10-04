
package com.analyticobjects.exercise2;

import java.security.SecureRandom;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * RandomProducer puts RandomProducer.LIMIT numbers into the DataStore.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
public class RandomProducer implements Runnable {
    
    private final DataStore randomNumberStorage = DataStore.getInstance();
    private final SecureRandom secureRandom = new SecureRandom();
    static final int LIMIT = 100;

    @Override
    public void run() {
        try {
            for (int i = 1; i <= LIMIT; i++) {
                randomNumberStorage.putNumber(secureRandom.nextInt());
            }
        } catch (InterruptedException ex) {
            Logger.getLogger(RandomProducer.class.getName()).log(Level.SEVERE, ex.getLocalizedMessage(), ex);
        }
    }
    
}
