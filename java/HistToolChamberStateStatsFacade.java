package com.sensoranalytics.inspectionmanager.facade;

import com.sensoranalytics.inspectionmanager.entity.HistToolChamberStateStats;
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
@Local(HistToolChamberStateStatsFacadeLocal.class)
@LocalBean
public class HistToolChamberStateStatsFacade extends AbstractFacade<HistToolChamberStateStats> implements HistToolChamberStateStatsFacadeLocal {

	@PersistenceContext(unitName = "IMPU")
	private EntityManager em;

	@Override
	protected EntityManager getEntityManager() {
		return em;
	}

	public HistToolChamberStateStatsFacade() {
		super(HistToolChamberStateStats.class);
	}


	@Override
	public List<HistToolChamberStateStats> getByStartDate(Date startDate) {
		TypedQuery<HistToolChamberStateStats> query = em.createNamedQuery(HistToolChamberStateStats.GET_BY_STARTDATE, HistToolChamberStateStats.class);
		query.setParameter(HistToolChamberStateStats.STARTDATE, startDate);
		List<HistToolChamberStateStats> histList;
		try {
			histList = query.getResultList();
		} catch (NoResultException ex) {
			histList = new ArrayList<>();
		}
		return histList;
	}


}
