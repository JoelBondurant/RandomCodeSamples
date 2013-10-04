package com.sensoranalytics.inspectionmanager.facade;

import com.sensoranalytics.inspectionmanager.entity.BaseEntity;
import java.util.Collection;
import java.util.List;
import javax.persistence.EntityManager;
import javax.persistence.TypedQuery;
import javax.persistence.criteria.CriteriaQuery;
import javax.persistence.criteria.Expression;
import javax.persistence.criteria.Root;

/**
 *
 * @author Joel Bondurant
 */
public abstract class AbstractFacade<T> {

	private Class<T> entityClass;

	public AbstractFacade(Class<T> entityClass) {
		this.entityClass = entityClass;
	}

	protected abstract EntityManager getEntityManager();

	public void create(T entity) {
		getEntityManager().persist(entity);
	}

	public void update(T entity) {
		getEntityManager().merge(entity);
	}

	public void delete(T entity) {
		getEntityManager().remove(getEntityManager().merge(entity));
	}

	public void bulkCreate(Collection<T> entityList) {
		for (T entity : entityList) {
			if (((BaseEntity) entity).getId() == null) {
				getEntityManager().persist(entity);
			}
		}
	}

	public void bulkUpdate(Collection<T> entityList) {
		for (T entity : entityList) {
			if (((BaseEntity) entity).getId() != null) {
				getEntityManager().merge(entity);
			}
		}
	}

	public void bulkDelete(Collection<T> entityList) {
		for (T entity : entityList) {
			getEntityManager().remove(getEntityManager().merge(entity));
		}
	}

	public T find(Object id) {
		return getEntityManager().find(entityClass, id);
	}

	public List<T> findAll() {
		CriteriaQuery<T> cq = getEntityManager().getCriteriaBuilder().createQuery(entityClass);
		cq.select(cq.from(entityClass));
		return getEntityManager().createQuery(cq).getResultList();
	}

	public int count() {
		CriteriaQuery<Long> cq = getEntityManager().getCriteriaBuilder().createQuery(Long.class);
		Root<T> rt = cq.from(entityClass);
		Expression<Long> count = getEntityManager().getCriteriaBuilder().count(rt);
		cq.select(count);
		TypedQuery<Long> tq = getEntityManager().createQuery(cq);
		return (tq.getSingleResult()).intValue();
	}

	public void bulkSync(Collection<T> entityList) {
		this.bulkCreate(entityList);
		this.bulkUpdate(entityList);
	}
}
