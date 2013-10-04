package com.sensoranalytics.inspectionmanager.facade;

import com.sensoranalytics.inspectionmanager.entity.Operation;
import javax.ejb.Local;
import javax.ejb.Remote;
import javax.ejb.Stateless;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;

/**
 *
 * @author Joel Bondurant
 */
@Stateless
@Remote(OperationFacadeRemote.class)
@Local(OperationFacadeLocal.class)
public class OperationFacade extends AbstractFacade<Operation> implements OperationFacadeLocal {

	@PersistenceContext(unitName = "IMPU")
	private EntityManager em;

	@Override
	protected EntityManager getEntityManager() {
		return em;
	}

	public OperationFacade() {
		super(Operation.class);
	}


}
