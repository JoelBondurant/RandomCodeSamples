package com.sensoranalytics.inspectionmanager.fileimport;

import com.sensoranalytics.commons.FileUtility;
import com.sensoranalytics.inspectionmanager.entity.FileImport;
import com.sensoranalytics.inspectionmanager.entity.Pipeline;
import com.sensoranalytics.inspectionmanager.entity.Stage;
import com.sensoranalytics.inspectionmanager.entity.SystemPreference;
import com.sensoranalytics.inspectionmanager.facade.*;
import com.sensoranalytics.logging.LogHandler;
import com.sensoranalytics.logging.LoggerFactory;
import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.*;

/**
 * The overall mechanics of processing files is here.
 * @author Joel Bondurant
 */
@Singleton
public class FileProcessor  {

	boolean isBusy = false;

	static final String LOG_ZONE = "FILE_IMPORT";
	private static final Logger logger = LoggerFactory.getLogger(LOG_ZONE);

	@EJB private FileImportFacadeLocal fileImportFacade;
	@EJB private PipelineFacadeLocal pipelineFacade;
	@EJB private StageFacadeLocal stageFacade;
	@EJB private FactoryDimensionProcessor factoryDimensionProcessor;
	@EJB private XmlEventProcessor xmlEventProcessor;
	@EJB private SystemPreferenceFacadeLocal systemPreferenceFacade;
	@EJB private MongoImport mongoImport;

	public boolean isBusy() {
		return this.isBusy;
	}

	public void setNotBusy() {
		this.isBusy = false;
	}

	public void setBusy() {
		this.isBusy = true;
	}

	//@Asynchronous
	@TransactionAttribute(TransactionAttributeType.NEVER)
	public void importFile(File fileToImport) {
		if (!fileToImport.exists()) {
			return;
		}
		logger.log(Level.INFO, "FileProcessor.importFile({0}).", fileToImport.getName());

		FileImport fileImport = start(fileToImport);
		fileImportFacade.create(fileImport);

		boolean fetchSuccess = fetch(fileImport);
		if (!fetchSuccess) {
			fileImportFacade.delete(fileImport);
			return;
		} else {
			fileImportFacade.update(fileImport);
		}
		boolean validateSuccess = validate(fileImport);
		fileImportFacade.update(fileImport);
		if (!validateSuccess) {
			fileImportFacade.fail(fileImport);
			return;
		}
		boolean digestSuccess = digest(fileImport);
		fileImportFacade.update(fileImport);
		if (!digestSuccess) {
			fileImportFacade.fail(fileImport);
			return;
		}
		finish(fileImport);
		fileImportFacade.update(fileImport);
		mongoImport.pumpData();
	}

	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	private FileImport start(File aFile) {
		Stage startStage = stageFacade.findByStageType(Stage.StageType.START);
		if (startStage == null) {
			SystemPreference sp = systemPreferenceFacade.findByKeyWithDefaultValue(FileImport.FILE_IMPORT_PICKUP_PATH_SYSTEMSETTING_KEY, FileImport.DEFAULT_FILE_IMPORT_PICKUP_PATH);
			String fileImportPath = sp.getPrefValue();
			startStage = new Stage(Stage.StageType.START, fileImportPath);
			stageFacade.create(startStage);
		}
		FileImport fileImport = new FileImport(startStage, aFile.getName());
		if (fileImport.getMD5Hash().isEmpty()) {
			fileImportFacade.fail(fileImport);
			logger.log(Level.SEVERE, "MD5Hash of file failed: {0}", Long.toString(fileImport.getId()));
			return null;
		}
		return fileImport;
	}

	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	private boolean fetch(FileImport fileImport) {
		logger.log(Level.INFO, "File in fetch stage: {0}", fileImport.toString());

		// Move file from pickup path to working path.
		String workingPath = FileImport.DEFAULT_FILE_IMPORT_WORKING_PATH;
		Stage fetchStage = stageFacade.findByStageType(Stage.StageType.FETCH);
		if (fetchStage == null) {
			fetchStage = new Stage(Stage.StageType.FETCH, workingPath);
			stageFacade.create(fetchStage);
		}
		try {
			File destDir = new File(FileImport.DEFAULT_FILE_IMPORT_WORKING_PATH);
			String fileName = FileUtility.moveFileToDirectoryWithRename(fileImport.getFile(), destDir);
			if (!fileName.equalsIgnoreCase(fileImport.getFileName())) {
				fileImport.setFileName(fileName);
			}
		} catch (IOException ex) {
			return false;
		}
		fileImport.setStage(fetchStage);

		// Setup pipelines:
		Pipeline facDimPipeline = pipelineFacade.findByName(FactoryDimensionPipeline.PIPELINE_NAME);
		if (facDimPipeline == null) {
			facDimPipeline = new Pipeline(FactoryDimensionPipeline.PIPELINE_NAME, FactoryDimensionPipeline.DESCRIPTION, FactoryDimensionPipeline.FILENAME_REGEX);
			pipelineFacade.create(facDimPipeline);
		}
		Pipeline xmlEventPipeline = pipelineFacade.findByName(XmlEventPipeline.PIPELINE_NAME);
		if (xmlEventPipeline == null) {
			xmlEventPipeline = new Pipeline(XmlEventPipeline.PIPELINE_NAME, XmlEventPipeline.DESCRIPTION, XmlEventPipeline.FILENAME_REGEX);
			pipelineFacade.create(xmlEventPipeline);
		}

		// Set pipeline based on file name:
		if (fileImport.getFileName().matches(facDimPipeline.getFileNameRegEx())) {
			fileImport.setPipeline(facDimPipeline);
		} else if (fileImport.getFileName().matches(xmlEventPipeline.getFileNameRegEx())) {
			fileImport.setPipeline(xmlEventPipeline);
		} else {
			fileImport.setStatus(FileImport.Status.STOPPED);
			return false;
		}

		// stop processing if file is a zero size.
		if (fileImport.isEmpty()) {
			fileImportFacade.fail(fileImport);
			fileImport.setStatus(FileImport.Status.EMPTY);
			fileImport.setIsValid(Boolean.TRUE);
			return false;
		}

		// stop processing if file is a duplicate.
		if (fileImportFacade.isDuplicate(fileImport)) {
			fileImportFacade.fail(fileImport);
			fileImport.setStatus(FileImport.Status.DUPLICATE);
			return false;
		}
		return true;
	}

	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	private boolean validate(FileImport fileImport) {
		logger.log(Level.INFO, "File in validate stage: {0}", fileImport.toString());
		Stage validateStage = stageFacade.findByStageType(Stage.StageType.VALIDATE);
		if (validateStage == null) {
			validateStage = new Stage(Stage.StageType.VALIDATE, fileImport.getFilePath());
			stageFacade.create(validateStage);
		}
		fileImport.setStage(validateStage);
		if (fileImport.getPipeline().getName().equals(XmlEventPipeline.PIPELINE_NAME)) {
			fileImport.setIsValid(Boolean.TRUE);
			return true;
		}
		FactoryDimensionPipeline facDimPipeline = new FactoryDimensionPipeline();
		List<String> validationRegExs = facDimPipeline.getValidationRegExs();
		FileValidator fileValidator = new FileValidator(fileImport.getFile());
		fileValidator.addLineRegExs(validationRegExs);
		boolean validationResult;
		try {
			validationResult = fileValidator.validateFile();
			fileImport.setIsValid(validationResult);
		} catch (IOException ex) {
			logger.severe(ex.toString());
			logger.severe(LogHandler.stackTrace(ex));
			fileImport.setIsValid(Boolean.FALSE);
			fileImportFacade.fail(fileImport);
			return false;
		}
		return validationResult;
	}

	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	private boolean digest(FileImport fileImport) {
		logger.log(Level.INFO, "File in digest stage: {0}", fileImport.toString());
		Stage digestStage = stageFacade.findByStageType(Stage.StageType.VALIDATE);
		if (digestStage == null) {
			digestStage = new Stage(Stage.StageType.DIGEST, fileImport.getFilePath());
			stageFacade.create(digestStage);
		}
		fileImport.setStage(digestStage);
		boolean digestSuccess;
		if (fileImport.getPipeline().getName().equals(FactoryDimensionPipeline.PIPELINE_NAME)) {
			try {
				digestSuccess = factoryDimensionProcessor.digest(fileImport);
			} catch (Exception ex) {
				logger.severe(ex.toString());
				logger.severe(LogHandler.stackTrace(ex));
				digestSuccess = false;
			}
		} else {
			try {
				digestSuccess = xmlEventProcessor.digest(fileImport);
			} catch (Exception ex) {
				logger.severe(ex.toString());
				logger.severe(LogHandler.stackTrace(ex));
				digestSuccess = false;
			}
		}
		if (!digestSuccess) {
			fileImportFacade.fail(fileImport);
		}
		return digestSuccess;
	}

	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	private void finish(FileImport fileImport) {
		Stage finishStage = stageFacade.findByStageType(Stage.StageType.FINISH);
		if (finishStage == null) {
			finishStage = new Stage(Stage.StageType.FINISH, fileImport.getFilePath());
			stageFacade.create(finishStage);
		}
		fileImport.setStage(finishStage);
		fileImport.setStatus(FileImport.Status.SUCCESS);
		fileImport.setTimeFinished(new Date());
		logger.log(Level.INFO, "File finished: {0}", fileImport.toString());
	}

}
