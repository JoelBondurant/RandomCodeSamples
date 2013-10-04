package com.analyticobjects.exercise1;

import java.util.Comparator;

/**
 * Sort FileDetails by file size in decreasing order.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
class FileDetailsComparator implements Comparator<FileDetails> {
    @Override
    public int compare(FileDetails fd1, FileDetails fd2) {
        long size1 = fd1.getSizeInBytes();
        long size2 = fd2.getSizeInBytes();
        if (size1 == size2) {
            return fd1.getFileName().compareTo(fd2.getFileName());
        }
        if (size1 > size2) {
            return -1;
        }
        return 1;
    }
}
