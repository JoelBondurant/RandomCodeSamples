package com.sensoranalytics.inspectionmanager.facade;

import com.sensoranalytics.inspectionmanager.entity.Lot;
import java.util.List;
import javax.ejb.Local;
import javax.ejb.LocalBean;
import javax.ejb.Stateless;
import javax.ejb.TransactionAttribute;
import javax.ejb.TransactionAttributeType;
import javax.persistence.EntityManager;
import javax.persistence.NoResultException;
import javax.persistence.PersistenceContext;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaBuilder;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Root;

/**
 *
 * @author Joel Bondurant
 */
@Stateless
@Local(LotFacadeLocal.class)
@LocalBean
public class LotFacade extends AbstractFacade<Lot> implements LotFacadeLocal {

	@PersistenceContext(unitName = "IMPU")
	private EntityManager em;

	@Override
	protected EntityManager getEntityManager() {
		return em;
	}

	public LotFacade() {
		super(Lot.class);
	}


	@Override
	@TransactionAttribute(TransactionAttributeType.REQUIRES_NEW)
	public Lot findByFactoryId(String factoryLotId) {
		TypedQuery<Lot> query = em.createNamedQuery(Lot.FIND_BY_FACTORYID, Lot.class);
		query.setParameter(Lot.FACTORYID, factoryLotId);
		Lot lot;
		try {
			lot = query.getSingleResult();
		} catch(NoResultException ex) {
			lot = null;
		}
		return lot;
	}

	@Override
	public List<Lot> findActive() {
		CriteriaBuilder cb = getEntityManager().getCriteriaBuilder();
		CriteriaQuery<Lot> cq = cb.createQuery(Lot.class);
		Root<Lot> lot = cq.from(Lot.class);
		cq.select(lot).where(cb.equal(lot.get("isFinished"), false));
		return getEntityManager().createQuery(cq).getResultList();
	}

}
