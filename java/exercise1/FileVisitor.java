package com.analyticobjects.exercise1;

import java.io.IOException;
import java.nio.file.FileVisitResult;
import java.nio.file.Path;
import java.nio.file.SimpleFileVisitor;
import java.nio.file.attribute.BasicFileAttributes;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Class to recursively print file listing.
 * @author Joel Bondurant
 * @since 2013.10.04
 */
class FileVisitor extends SimpleFileVisitor<Path> {
    private final List<FileDetails> fileDetailsList = new ArrayList<>();

    @Override
    public FileVisitResult visitFile(Path aPath, BasicFileAttributes fileAttributes) throws IOException {
      //System.out.println("Processing file:" + aPath);
      fileDetailsList.add(new FileDetails(aPath));
      return FileVisitResult.CONTINUE;
    }

    @Override
    public FileVisitResult preVisitDirectory(Path aPath, BasicFileAttributes fileAttributes) throws IOException {
      return FileVisitResult.CONTINUE;
    }

    /**
     * Getter for the sorted file details listing of the files visited.
     * @return Sorted file details.
     */
    List<FileDetails> getFileDetailsListing() {
        Collections.sort(fileDetailsList, new FileDetailsComparator());
        return this.fileDetailsList;
    }
}
