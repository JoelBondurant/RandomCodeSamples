package com.analyticobjects.exercise1;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Exercise 1.
 * 
 * Please write a program that can read the contents of any directory (and it’s subdirectories) in the
 * filesystem, and display the contents sorted in order of file size to System.out. The directory to
 * search should be passed as a parameter to the “main” method of the program.
 * The output should show the full path of the file, the file name, and the file size.
 * 
 * @author Joel Bondurant
 * @since 2013.10.04
 */
public class ExerciseOne {
    
    private final FileVisitor fileVisitor;

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        String pathToList = "./";
        if (args.length != 0) {
            pathToList = args[0];
        }
        ExerciseOne exercise1 = new ExerciseOne();
        try {
            Files.walkFileTree(Paths.get(pathToList), exercise1.fileVisitor);
            List<FileDetails> fileDetailsListing = exercise1.fileVisitor.getFileDetailsListing();
            for (FileDetails fileDetails : fileDetailsListing) {
                System.out.println(fileDetails.getDescription());
            }
        } catch (IOException ex) {
            Logger.getLogger(ExerciseOne.class.getName()).log(Level.SEVERE, ex.getLocalizedMessage(), ex);
        }
    }
    
    /**
     * Constructor for internal use only.
     */
    private ExerciseOne() {
        this.fileVisitor = new FileVisitor();
    }
    
}
