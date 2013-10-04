package com.sensoranalytics.inspectionmanager.facade;

import com.sensoranalytics.inspectionmanager.entity.FileImport;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import javax.ejb.Local;
import javax.ejb.LocalBean;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;

/**
 *
 * @author Joel Bondurant
 */
@Stateless
@Local(FileImportFacadeLocal.class)
@LocalBean
public class FileImportFacade extends AbstractFacade<FileImport> implements FileImportFacadeLocal {

	@PersistenceContext(unitName = "IMPU")
	private EntityManager em;

	@Override
	protected EntityManager getEntityManager() {
		return em;
	}

	public FileImportFacade() {
		super(FileImport.class);
	}

	@Override
	public void fail(FileImport fileImport) {
		fileImport.setStatus(FileImport.Status.FAILURE);
		fileImport.setTimeFinished(new Date());
		update(fileImport);
	}

	/**
	 * A method to determine whether this file has already been imported successfully.
	 * @return True if a file import with the same md5 hash already exists for a successful import, false otherwise.
	 */
	@Override
	public boolean isDuplicate(FileImport fileImport) {
		TypedQuery<FileImport> query = em.createNamedQuery(FileImport.FIND_BY_MD5HASH_STATUS, FileImport.class);
		query.setParameter(FileImport.MD5HASH, fileImport.getMD5Hash());
		query.setParameter(FileImport.STATUS, FileImport.Status.SUCCESS);
		try {
			List<FileImport> fis;
			fis = query.getResultList();
			if (fis.size() > 0) {
				return true;
			}
		} catch(NoResultException ex) {
			return false;
		}
		return false;
	}

	@Override
	public List<FileImport> findByNotInMongo() {
		TypedQuery<FileImport> query = em.createNamedQuery(FileImport.FIND_BY_NOT_INMONGO, FileImport.class);
		List<FileImport> fis = new ArrayList<>();
		try {
			for (FileImport fi : query.getResultList()) {
				if (fi.getStatus() == FileImport.Status.SUCCESS) {
					fis.add(fi);
				}
			}
		} catch(NoResultException ex) {
		}
		return fis;
	}


}
