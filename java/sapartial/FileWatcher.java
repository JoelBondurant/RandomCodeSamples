package com.sensoranalytics.inspectionmanager.fileimport;

import com.sensoranalytics.commons.FileUtility;
import com.sensoranalytics.commons.TimeUtility;
import com.sensoranalytics.inspectionmanager.entity.FileImport;
import com.sensoranalytics.inspectionmanager.entity.SystemPreference;
import com.sensoranalytics.inspectionmanager.facade.SystemPreferenceFacadeLocal;
import com.sensoranalytics.logging.LogHandler;
import com.sensoranalytics.logging.LoggerFactory;
import java.io.File;
import java.io.RandomAccessFile;
import java.nio.channels.FileChannel;
import java.nio.channels.FileLock;
import java.util.*;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;


/**
 * A class to poll/watch for files and trigger processing.
 * @author Joel Bondurant
 */
@Stateless
public class FileWatcher implements FileWatcherLocal {

	static {System.out.println("FileWatcher classloader called.");}

	private static final Logger logger = LoggerFactory.getLogger(FileProcessor.LOG_ZONE);
	@EJB private SystemPreferenceFacadeLocal systemPreferenceFacade;
	@EJB private FileProcessor fileProcessor;

	public static final String STOP_PREF_KEY = "FileImportStop";
	public static final String STOP = "STOP";
	public static final String GO = "GO";


	//@Schedule(second = "*/20", minute = "*", hour = "*", persistent=false)
	@Override
	@TransactionAttribute(TransactionAttributeType.NEVER)
	public void checkForFiles() {
		logger.info("FileWatcher.checkForFiles:start");
		if (fileProcessor.isBusy()) {
			logger.info("FileProcessor is busy.");
			return;
		}
		SystemPreference sp = systemPreferenceFacade.findByKeyWithDefaultValue(STOP_PREF_KEY, GO);
		String stopPref = sp.getPrefValue();
		if (stopPref.equals(STOP)) {
			return;
		}
		sp = systemPreferenceFacade.findByKeyWithDefaultValue(FileImport.FILE_IMPORT_PICKUP_PATH_SYSTEMSETTING_KEY, FileImport.DEFAULT_FILE_IMPORT_PICKUP_PATH);
		String fileImportPath = sp.getPrefValue();
		File fileImportFileObj = new File(fileImportPath);
		Collection<File> files = FileUtility.listFiles(fileImportFileObj, null, false);
		if (files.isEmpty()) {
			return; // if no files, do nothing.
		}
		List<File> fileList = new ArrayList<>(files);
		Collections.sort(fileList, new FileComparator()); // sort files to process in order.
		Date dtNow = new Date();
		/* This following stuff is an attempt to tell if a file is busy, but it doesn't work well
		due to platform dependent file locking.
		*/
		for (File aFile: fileList) {
			if ((!aFile.canWrite()) || (aFile.lastModified() == 0L) || TimeUtility.timeDifferenceInSeconds(new Date(aFile.lastModified()), dtNow) < 10) {
				return; // if any of the files were modified within the past 10 sec, skip.
			}
		}
		for (File aFile: fileList) {
			try (FileChannel fileChannel = new RandomAccessFile(aFile, "rw").getChannel()) {
				FileLock fileLock = fileChannel.lock(); // Get an exclusive lock on the whole file
				fileLock.release();
			} catch (Exception ex) {
				logger.severe(ex.toString());
				logger.severe(LogHandler.stackTrace(ex));
				return;
			}
		}

		File aFile = fileList.get(0); // only take 1 file per call.
		fileProcessor.setBusy();
		try {
			fileProcessor.importFile(aFile);
		} catch (Exception ex) {
			logger.info("FileProcessor.importFile:FAIL");
		} finally {
			fileProcessor.setNotBusy();
		}
		logger.info("FileWatcher.checkForFiles:end");
	}

	/**
	 * Sort files to process by factory dimension, then event files in order of increasing date stamp.
	 */
	private class FileComparator implements Comparator<File> {
		@Override
		public int compare(File f1, File f2) {
			String fn1 = f1.getName();
			String fn2 = f2.getName();
			String f1ds, f2ds;
			if (fn1.matches(XmlEventPipeline.FILENAME_REGEX)) {
				f1ds = "b" + fn1.substring(XmlEventPipeline.LengthOfFileNamePrefix);
			} else if (fn1.matches(FactoryDimensionPipeline.FILENAME_REGEX)) {
				f1ds = "a" + fn1.substring(FactoryDimensionPipeline.LengthOfFileNamePrefix);
			} else {
				return -1;
			}
			if (fn2.matches(XmlEventPipeline.FILENAME_REGEX)) {
				f2ds = "b" + fn2.substring(XmlEventPipeline.LengthOfFileNamePrefix);
			} else if (fn2.matches(FactoryDimensionPipeline.FILENAME_REGEX)) {
				f2ds = "a" + fn2.substring(FactoryDimensionPipeline.LengthOfFileNamePrefix);
			} else {
				return 1;
			}
			return f1ds.compareToIgnoreCase(f2ds);
		}
	}


}
