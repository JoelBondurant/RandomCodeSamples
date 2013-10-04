package com.analyticobjects.exercise1;

import java.io.File;
import java.nio.file.Path;

/**
 * A class to house information on our files.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
class FileDetails {
    private final long sizeInBytes;
    private final String description;
    private final String fileName;

    /**
     * Construct details on a file from it's path.
     * @param aPath 
     */
    FileDetails(Path aPath) {
        File aFile = aPath.toFile();
        this.sizeInBytes = aFile.length();
        this.fileName = aPath.getFileName().toString();
        this.description = aFile.getAbsolutePath() + ", " + this.fileName + ", " + Long.toString(this.sizeInBytes) + " bytes.";
    }

    long getSizeInBytes() {
        return this.sizeInBytes;
    }

    String getDescription() {
        return this.description;
    }

    String getFileName() {
        return this.fileName;
    }
}
