package com.sensoranalytics.commons;

import java.io.File;
import java.io.IOException;
import java.io.Serializable;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;


/**
 * This class is a helper utility for common file operations, primarily needed until Java 7's JSR 203.
 * Added inheritance from Apache commons IO's FileUtils and removed boilerplate methods.
 *
 * @author Joel Bondurant
 * @version 2011.0316
 * @since 1.0
 */
public class FileUtility extends FileUtils implements Serializable {

	private FileUtility() {}  // makes sure that no one tries to instantiate this.

	/**
	 * Moves a file and if the destination has a file of the same name, it will find the lowest integer
	 * n such that the filename with (n) appended just before the file extension is untaken and use
	 * that name.
	 * @param srcFile The source file to move.
	 * @param destDir The destination directory.
	 * @return A string of the new file name.
	 * @throws IOException
	 */
	public static String moveFileToDirectoryWithRename(File srcFile, File destDir) throws IOException {
		String srcAbsolutePath = srcFile.getAbsolutePath();
		String baseName = FilenameUtils.getBaseName(srcAbsolutePath);
		String fileExt = FilenameUtils.getExtension(srcAbsolutePath);
		String srcFileName = srcFile.getName();
		File destFile;
		destFile = new File(destDir, srcFileName);
		if (!destFile.exists()) {
			FileUtils.moveFileToDirectory(srcFile, destDir, true);
			return destFile.getName();
		}
		for(int i = 1; true; i++) {
			destFile = new File(destDir, baseName + "(" + Integer.toString(i) + ")" + FilenameUtils.EXTENSION_SEPARATOR_STR + fileExt);
			if (!destFile.exists()) {
				FileUtils.moveFile(srcFile, destFile);
				return destFile.getName();
			}
		}
	}

}