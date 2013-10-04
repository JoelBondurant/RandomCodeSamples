package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import java.util.Date;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;

/**
 *
 * @author Joel Bondurant
 */
@Entity
@Table(name = "ProcessBatch")
public class ProcessBatch implements BaseEntity, Serializable {

	private static final long serialVersionUID = 1L;

	@Id
    @Basic(optional = false)
    @NotNull
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

    @Temporal(TemporalType.TIMESTAMP)
	private Date endTime;

    @Temporal(TemporalType.TIMESTAMP)
	private Date startTime;

    @Temporal(TemporalType.TIMESTAMP)
	private Date tNow;

	@Size(max = 255)
	private String type;

	protected ProcessBatch() {
	}

	public ProcessBatch(Date startTime, Date tNow, String type) {
		this();
		this.startTime = (Date) startTime.clone();
		this.tNow = (Date) tNow.clone();
		this.type = type;
	}

	@Override
	public Long getId() {
		return id;
	}

	public Date getEndTime() {
		return (Date) endTime.clone();
	}

	public void setEndTime(Date endTime) {
		this.endTime = (Date) endTime.clone();
	}

	public Date getStartTime() {
		return (Date) startTime.clone();
	}

	public void setStartTime(Date startTime) {
		this.startTime = (Date) startTime.clone();
	}

	public Date getTnow() {
		return (Date) tNow.clone();
	}

	public void setTnow(Date tNow) {
		this.tNow = (Date) tNow.clone();
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	@Override
	public int hashCode() {
		int hash = 0;
		hash += (id != null ? id.hashCode() : 0);
		return hash;
	}

	@Override
	public boolean equals(Object object) {
		if (!(object instanceof ProcessBatch)) {
			return false;
		}
		ProcessBatch other = (ProcessBatch) object;
		if ((this.id == null && other.id != null) || (this.id != null && !this.id.equals(other.id))) {
			return false;
		}
		return true;
	}

	@Override
	public String toString() {
		return "com.sensoranalytics.inspectionmanager.entity.ProcessBatch[ id=" + id + " ]";
	}

}
