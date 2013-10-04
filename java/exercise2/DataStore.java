package com.analyticobjects.exercise2;

import java.util.concurrent.LinkedBlockingQueue;

/**
 * Abstraction to hide number storage mechanism. This class is thread safe
 * and designed for publisher/subscriber usage as it implements BlockingQueue.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
class DataStore extends LinkedBlockingQueue<Integer> {
    
    private static DataStore singleton;
    private DataStore() {}
    
    static synchronized DataStore getInstance() {
        if (singleton == null) {
            singleton = new DataStore();
        }
        return singleton;
    }
    
    /**
     * Put a integer in the collection.
     * @param anInt An integer to store.
     * @throws InterruptedException 
     */
    void putNumber(int anInt) throws InterruptedException {
        this.put(anInt);
    }
    
    /**
     * Take a number from the collection, waiting if necessary.
     * @return An integer from the collection.
     * @throws InterruptedException 
     */
    int takeNumber() throws InterruptedException {
        return this.take();
    }
}
