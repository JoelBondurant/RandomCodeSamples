package com.sensoranalytics.inspectionmanager.entity;

import com.sensoranalytics.commons.ByteUtility;
import java.io.*;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import org.apache.commons.io.IOUtils;

/**
 *
 * @author Joel Bondurant
 */
@Entity
@Table(name = "FileImport")
@NamedQueries({
	@NamedQuery(name = FileImport.FIND_BY_MD5HASH_STATUS, query = "SELECT f FROM FileImport f WHERE f.md5Hash = :md5Hash AND f.status = :status"),
	@NamedQuery(name = FileImport.FIND_BY_NOT_INMONGO, query = "SELECT f FROM FileImport f WHERE f.inMongo = 0")})
public class FileImport implements BaseEntity, Serializable {

	private static final long serialVersionUID = 1L;
	public static final String FIND_BY_MD5HASH_STATUS = "FileImport.findByMD5HashStatus";
	public static final String FIND_BY_NOT_INMONGO = "FileImport.findByNotInMongo";
	public static final String MD5HASH = "md5Hash";
	public static final String STATUS = "status";

	static final String LOG_ZONE = "FILE_IMPORT";
	//private static final java.util.logging.Logger logger = LoggerFactory.getLogger(LOG_ZONE);

	/**
	 * The default path where files are picked up for processing. This is overridden by persisting a SystemSetting.
	 */
	public static final String DEFAULT_FILE_IMPORT_PICKUP_PATH = "C:\\SensorAnalytics\\trunk\\Deployment\\root\\pickup";
	/**
	 * The default path where files are stored during processing and until archived. This is overridden by persisting a SystemSetting.
	 */
	public static final String DEFAULT_FILE_IMPORT_WORKING_PATH = "C:\\SensorAnalytics\\trunk\\Deployment\\root\\working";
	/**
	 * The default path where files are stored during processing and until archived. This is overridden by persisting a SystemSetting.
	 */
	public static final String DEFAULT_FILE_IMPORT_ARCHIVE_PATH = "C:\\SensorAnalytics\\trunk\\Deployment\\root\\archive";
	/**
	 * Key to the SystemSetting for the path where files are picked up.
	 */
	public static final String FILE_IMPORT_PICKUP_PATH_SYSTEMSETTING_KEY = "FileImportPickupPath";
	/**
	 * Key to the SystemSetting for the file import working path where file data is stored during
	 * processing and until archived.
	 */
	public static final String FILE_IMPORT_WORKING_PATH_SYSTEMSETTING_KEY = "FileImportWorkingPath";
	/**
	 * Key to the SystemSetting for the file import archive path where files will be archived.
	 */
	public static final String FILE_IMPORT_ARCHIVE_PATH_SYSTEMSETTING_KEY = "FileImportArchivePath";
	@Id
	@Basic(optional = false)
	@NotNull
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;
	@Basic(optional = false)
	@NotNull
	@Size(min = 1, max = 100)
	private String fileName;
	@Basic(optional = false)
	@NotNull
	private Long fileSizeInBytes;
	@Basic(optional = false)
	@NotNull
	@Size(min = 1, max = 255)
	private String md5Hash;
	@Basic(optional = false)
	@NotNull
	@Enumerated(EnumType.STRING)
	private Status status;
	@Temporal(TemporalType.TIMESTAMP)
	private Date timeFinished;
	@Basic(optional = false)
	@NotNull
	@Temporal(TemporalType.TIMESTAMP)
	private Date timeReceived;
	private Boolean isValid;
	private Boolean inMongo;

	@ManyToOne()
	private Pipeline pipeline;

	@ManyToOne()
	private Stage stage;

	protected FileImport() {
		this.isValid = null;
		this.inMongo = Boolean.FALSE;
	}

	/**
	 * FileImport constructor.
	 * @param fileName The name of the file received without path.
	 */
	public FileImport(Stage stage, String fileName) {
		this();
		this.stage = stage;
		this.timeReceived = new Date();
		this.status = Status.PROCESSING;
		this.fileName = fileName;
		this.fileSizeInBytes = getFile().length();
		this.md5Hash = this.computeMd5Hash(getFile());
	}


	@Override
	public Long getId() {
		return id;
	}

	/**
	 * File import status setter.
	 * @param status The status of the file import.
	 * @return this.
	 */
	public FileImport setStatus(Status status) {
		this.status = status;
		return this;
	}

	/**
	 * File import status getter.
	 * @return The status of the file import.
	 */
	public Status getStatus() {
		return this.status;
	}

	public Long getFileSizeInBytes() {
		return this.fileSizeInBytes;
	}

	/**
	 * File name getter.
	 * @return The file name of the file being imported.
	 */
	public String getFileName() {
		return this.fileName;
	}

	/**
	 * File import stage setter.
	 * @param stage The stage to set the import to.
	 * @return this.
	 */
	public FileImport setStage(Stage stage) {
		this.stage = stage;
		return this;
	}

	/**
	 * File import stage getter.
	 * @return The stage of this file import.
	 */
	public Stage getStage() {
		return this.stage;
	}

	/**
	 * File import pipeline getter.
	 * @return The pipeline for this import.
	 */
	public Pipeline getPipeline() {
		return this.pipeline;
	}

	public void setPipeline(Pipeline pipeline) {
		this.pipeline = pipeline;
	}

	/**
	 * Instantiates a new File object for the file being processed based on the path of the
	 * current stage and current file name.
	 * @return A file object pointing to the file being processed.
	 */
	public final File getFile() {
		return new File(stage.getFilePath() + File.separator + this.fileName);
	}

	public String getMD5Hash() {
		return this.md5Hash;
	}

	/**
	 * File path getter.
	 * @return The parent file path of the file being imported.
	 */
	public String getFilePath() {
		return this.stage.getFilePath();
	}

	/**
	 * File name setter.
	 * @param fileName The name of the file being imported.
	 */
	public void setFileName(String fileName) {
		this.fileName = fileName;
	}

	/**
	 * Method to determine if the file import has no data to process.
	 * @return true = file is empty; has zero bytes.
	 */
	public boolean isEmpty() {
		return this.fileSizeInBytes == 0L;
	}

	public Date getTimeFinished() {
		return (Date) timeFinished.clone();
	}

	public void setTimeFinished(Date timeFinished) {
		this.timeFinished = (Date) timeFinished.clone();
	}

	public Date getTimeReceived() {
		return (Date) timeReceived.clone();
	}

	public void setTimeReceived(Date timeReceived) {
		this.timeReceived = (Date) timeReceived.clone();
	}

	public void setInMongo() {
		this.inMongo = Boolean.TRUE;
	}

	public Boolean isValid() {
		return isValid;
	}

	public void setIsValid(Boolean isValid) {
		this.isValid = isValid;
	}

		/**
	 * Computes a readable string version of the md5 hash for a file. This hash is used to detect
	 * duplicate file imports. Only one file of the same hash will be processed. A workaround to this
	 * is to pad the file with empty lines which will be ignored, but change the hash.
	 * @param aFile The file to hash.
	 * @return The md5 hash as a readable string.
	 */
	public final String computeMd5Hash(File aFile) {
		FileInputStream inStream = null;
		byte[] fileBytes = null;
		byte[] byteBlock = null;
		try {
			inStream = new FileInputStream(aFile);
			fileBytes = new byte[(int)aFile.length()];
			inStream.read(fileBytes);
			MessageDigest msgDigest = MessageDigest.getInstance("MD5");
			byteBlock = msgDigest.digest(fileBytes);
			// TODO: fix this eh...
		} catch (NoSuchAlgorithmException | IOException ex) {
			System.err.println(ex.toString());
		} finally {
			IOUtils.closeQuietly(inStream);
		}
		if (byteBlock == null) {
			return "NULL";
		}
		return ByteUtility.toHexString(byteBlock);
	}

	@Override
	public int hashCode() {
		int hash = 0;
		hash += (id != null ? id.hashCode() : 0);
		return hash;
	}

	@Override
	public boolean equals(Object object) {
		// TODO: Warning - this method won't work in the case the id fields are not set
		if (!(object instanceof FileImport)) {
			return false;
		}
		FileImport other = (FileImport) object;
		if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
			return false;
		}
		return true;
	}

	@Override
	public String toString() {
		return "FileImport[ id=" + id + ", name=" + this.fileName + " ]";
	}

	public void setId(long id) {
		this.id = id;
	}

	public enum Status implements Serializable {
		/**
		 * File import processing has completed successfully, this should only happen by the FinishStage.
		 */
		SUCCESS,
		/**
		 * File import processing is in progress.
		 */
		PROCESSING,
		/**
		 * A file with the same hash has already been processed.
		 */
		DUPLICATE,
		/**
		 * The file contained zero bytes of data.
		 */
		EMPTY,
		/**
		 * An exception has led to the failure of file processing.
		 */
		FAILURE,
		/**
		 * File processing was stopped according to plan.
		 */
		STOPPED
	}
}
