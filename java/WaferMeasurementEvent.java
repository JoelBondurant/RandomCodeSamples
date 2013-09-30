package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import javax.persistence.*;
import javax.validation.constraints.NotNull;

/**
 * A class to represent wafer measurement events.
 *
 * @author Joel Bondurant
 * @version 2012.0514
 * @since 1.0
 */
@Entity
@Table(
        name = "WaferMeasurementEvent"
)
public class WaferMeasurementEvent implements BaseEntity, Serializable, Comparable<WaferMeasurementEvent> {

	private static final long serialVersionUID = 1L;
	protected static final String FIND_RECENT_BY_DATE = "WaferMeasurementEvent.findRecentByDate";

	/**
	 * Primary Id.
	 */
	@Id
    @Basic(optional = false)
    @NotNull
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

	@ManyToOne(fetch = FetchType.EAGER, optional = true)
	@JoinColumn(name = "WAFER_ID")
	private Wafer wafer;

	@OneToOne(fetch = FetchType.EAGER, optional = true)
	@JoinColumn(name = "TOOLCHAMBER_ID")
	private ToolChamber toolChamber;

	@OneToOne(fetch = FetchType.EAGER, optional = true)
	@JoinColumn(name = "ADDEROPERATION_ID")
	private Operation adderOperation;

	private Double areaInspected;

	@OneToOne(fetch = FetchType.EAGER, cascade = CascadeType.ALL, optional = false)
	private WaferMeasurementMetric waferMeasurementMetric;

	protected WaferMeasurementEvent() { }


	public WaferMeasurementEvent(Wafer wafer, ToolChamber toolChamber, Operation adderOperation, Double areaInspected, WaferMeasurementMetric waferMeasurementMetric) {
		this();
		this.wafer = wafer;
		this.toolChamber = toolChamber;
		this.adderOperation = adderOperation;
		this.areaInspected = areaInspected;
		this.waferMeasurementMetric = waferMeasurementMetric;
	}

	@Override
	public Long getId() {
		return this.id;
	}

	public ToolChamber getToolChamber() {
		return this.toolChamber;
	}


	public Operation getAdderOperation() {
		return this.adderOperation;
	}

	public Wafer getWafer() {
		return this.wafer;
	}

	public Double getAreaInspected() {
		return this.areaInspected;
	}

	public WaferMeasurementMetric getWaferMeasurementMetric() {
		return this.waferMeasurementMetric;
	}
	
	@Override
    public boolean equals(Object obj) {
        if (!(obj instanceof WaferMeasurementEvent)) {
        	return false;
        }
        WaferMeasurementEvent other = (WaferMeasurementEvent) obj;
        return (this.hashCode() == other.hashCode());
    }

    @Override
    public int hashCode() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.toolChamber.getFactoryId()).append("_");
		sb.append(this.wafer.getFactoryId()).append("_");
		sb.append(this.adderOperation.getFactoryId()).append("_");
		// sb.append(this.waferMeasurementMetric.); // include all fields.
		return sb.toString().hashCode();
    }


	@Override
	public int compareTo(WaferMeasurementEvent otherWaferMeasurementEvent) {
		return this.toolChamber.getFactoryId().compareTo(otherWaferMeasurementEvent.toolChamber.getFactoryId());
	}

}
