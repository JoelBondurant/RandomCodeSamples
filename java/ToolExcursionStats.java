package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import javax.persistence.Entity;
import javax.persistence.FetchType;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.persistence.UniqueConstraint;

/**
 *
 * @author Joel Bondurant
 */
@Entity
@Table(name = "ToolExcursionStats", uniqueConstraints = @UniqueConstraint(columnNames = {"TOOL_ID"}))
public class ToolExcursionStats implements BaseEntity, Serializable {

	private static final long serialVersionUID = 1L;

	@Id
    @GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

	@OneToOne(fetch = FetchType.EAGER)
	private Tool tool;

	private double p_ExcNS;

	protected ToolExcursionStats() {
		this.p_ExcNS = 1.0;
	}

	public ToolExcursionStats(Tool tool) {
		this();
		this.tool = tool;
	}

	@Override
	public Long getId() {
		return this.id;
	}

	public Tool getTool() {
		return this.tool;
	}

	public Double getPExcNS() {
		return this.p_ExcNS;
	}

	public void setPExcNS(double p_ExcNS) {
		this.p_ExcNS = p_ExcNS;
	}

	public static String generateMapKey(Tool tool) {
		return tool.getId().toString();
	}

	@Override
	public String toString() {
		return "com.sensoranalytics.inspectionmanager.entity.ToolExcursionStats[ id=" + id + " ]";
	}

}
