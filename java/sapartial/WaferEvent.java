package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import java.util.Date;
import java.util.HashSet;
import java.util.Set;
import javax.persistence.*;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Null;
import javax.validation.constraints.Size;

/**
 * A class to represent wafer events.
 *
 * @author Joel Bondurant
 * @version 2011.0421
 * @since 1.0
 */
@Entity
@Table(
        name = "WaferEvent",
        uniqueConstraints = @UniqueConstraint(columnNames = {"TYPE", "DATEANDTIME", "WAFER_ID", "PRODUCT_ID", "OPERATION_ID", "TOOLCHAMBER_ID"})
)
@NamedQueries({
	@NamedQuery(name = WaferEvent.FIND_RECENT_BY_DATE, query = "select we from WaferEvent we where we.dateAndTime >= :aDate")
})
public class WaferEvent implements BaseEntity, Serializable, Comparable<WaferEvent> {

	private static final long serialVersionUID = 1L;
	protected static final String FIND_RECENT_BY_DATE = "WaferEvent.findRecentByDate";

	/**
	 * Primary Id.
	 */
	@Id
    @Basic(optional = false)
    @NotNull
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;

	@Enumerated(EnumType.STRING)
	@NotNull
	private Type type;

	@NotNull
	@Temporal(TemporalType.TIMESTAMP)
	private Date dateAndTime;

	@Null
	@Size(min = 1, max = 50)
	private String productUse;

	@NotNull
	@ManyToOne(fetch = FetchType.EAGER, optional = false)
	@JoinColumn(name = "WAFER_ID")
	private Wafer wafer;

	@NotNull
	@OneToOne(fetch = FetchType.EAGER, optional = false)
	@JoinColumn(name = "PRODUCT_ID")
	private Product product;

	@OneToOne(fetch = FetchType.EAGER)
	@JoinColumn(name = "NEXTPRODUCT_ID")
	private Product nextProduct;

	@NotNull
	@OneToOne(fetch = FetchType.EAGER, optional = false)
	@JoinColumn(name = "TOOLCHAMBER_ID")
	private ToolChamber toolChamber;

	@OneToOne(fetch = FetchType.EAGER)
	@JoinColumn(name = "NEXTTOOLCHAMBER_ID")
	private ToolChamber nextToolChamber;

	@NotNull
	@OneToOne(fetch = FetchType.EAGER, optional = false)
	@JoinColumn(name = "OPERATION_ID")
	private Operation operation;

	@OneToOne(fetch = FetchType.EAGER)
	@JoinColumn(name = "NEXTOPERATION_ID")
	private Operation nextOperation;

	@OneToMany(fetch = FetchType.LAZY)
	private Set<Tag> samplingTags;

	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "SAMPLINGMETHOD_ID")
	private SamplingMethod samplingMethod;

	@NotNull
	private Boolean getsProcessed;

	@Null
	private Integer slot;

	@NotNull
	private Long fileImportId;

	protected WaferEvent() {
		this.samplingTags = new HashSet<>();
	}

	/**
	 * Constructor.
	 * @param waferEventTypeId The wafer event type identifier.
	 * @param dateAndTime The time of the event.
	 * @param productUse The product use code associated with the event.
	 * @param toolChamber The tool chamber associated with the event.
	 * @param product The product associated with the event.
	 * @param nextProduct The next product associated with the event.
	 * @param recipe The recipe associated with the event.
	 * @param operation The operation associated with the event.
	 * @param nextOperation The next operation associated with the event.
	 * @param samplingTags The sampling tags associated with the event.
	 * @param getsProcessed Boolean flag to determine how the event is processed.
	 * @param fileImportId Link to the file import which created the event.
	 */
	public WaferEvent(String waferEventTypeId, Wafer wafer, Date dateAndTime, Integer slot, String productUse,
					ToolChamber toolChamber, ToolChamber nextToolChamber, Product product, Product nextProduct,
					Operation operation, Operation nextOperation, Set<Tag> samplingTags,
					Boolean getsProcessed, Long fileImportId) {
		this();
		this.type = Type.valueOf(waferEventTypeId);
		this.wafer = wafer;
		this.slot = slot;
		this.dateAndTime = dateAndTime;
		this.productUse = productUse;
		this.toolChamber = toolChamber;
		this.nextToolChamber = nextToolChamber;
		this.product = product;
		this.nextProduct = nextProduct;
		this.operation = operation;
		this.nextOperation = nextOperation;
		this.samplingTags.addAll(samplingTags);
		this.fileImportId = fileImportId;
		//this.samplingMethod = Factory.getInstance().getSamplingMethodByTags(samplingTags);
		this.getsProcessed = getsProcessed;
		if (!product.getFlow().containsOperation(operation)) {
			String msg = "WaferEvent::Product/Operation mismatch: (";
			msg += (product==null?"":product.getPDFId());
			msg += "/" + (operation==null?"":operation.getFactoryId()) + ")";
			throw new IllegalArgumentException(msg);
		}
		if (nextProduct != null && nextOperation != null && !nextProduct.getFlow().containsOperation(nextOperation)) {
			String msg = "WaferEvent::NextProduct/NextOperation mismatch: (";
			msg += (nextProduct==null?"":nextProduct.getPDFId());
			msg += "/" + (nextOperation==null?"":nextOperation.getFactoryId()) + ")";
			throw new IllegalArgumentException(msg);
		}
	}

	@Override
	public Long getId() {
		return this.id;
	}

	/**
	 * Type getter.
	 * @return The type of this.
	 */
	public Type getType() {
		return this.type;
	}

	public Boolean getsProcessed() {
		return this.getsProcessed;
	}

	public boolean matches(WaferEvent evt) {
		if (evt.operation.matches(this.operation) && evt.type == this.type) {
			return true;
		}
		return false;
	}

	public ToolChamber getToolChamber() {
		return this.toolChamber;
	}

	public ToolChamber getNextToolChamber() {
		return this.nextToolChamber;
	}

	public Operation getOperation() {
		return this.operation;
	}

	public Integer getSlot() {
		return this.slot;
	}

	public Operation getNextOperation() {
		return this.nextOperation;
	}

	public SamplingMethod getSamplingMethod() {
		return this.samplingMethod;
	}

	public Date getDateAndTime() {
		return this.dateAndTime;
	}

	public Product getProduct() {
		return this.product;
	}

	public Step getStep() {
		return this.product.getFlow().getStep(this.operation);
	}

	public Set<Tag> getSamplingTags() {
		return this.samplingTags;
	}

	public Wafer getWafer() {
		return this.wafer;
	}


	public void setProduct(Product product) {
		this.product = product;
	}

	public Product getNextProduct() {
		return this.nextProduct;
	}

	public boolean isNextInfoValid() {
		if (nextProduct != null && nextOperation != null) {
			boolean containsOperation = nextProduct.getFlow().containsOperation(nextOperation);
			return containsOperation;
		}
		return false;
	}

	@Override
	public String toString() {
		StringBuilder sb = new StringBuilder();
		sb.append(WaferEvent.class.getName());
		sb.append("(HASH:").append(Integer.toString(hashCode())).append("):");
		if (this.id != null) {
			sb.append("(ID:").append(Long.toString(this.id)).append("):");
		}
		sb.append("(TYPE:").append(this.type.name()).append(") ");
		sb.append("(LOT:").append(this.wafer.getLot().getFactoryId()).append(") ");
		sb.append("(WAFER:").append(this.wafer.getFactoryId()).append(") ");
		sb.append("(PRODUCT:").append(this.product.getPDFId()).append(") ");
		sb.append("(OPERATION:").append(this.operation.getFactoryId()).append(")");
		if (this.toolChamber != null) {
			sb.append(" (TOOLCHAMBER:").append(this.toolChamber.getFactoryId()).append(")");
		}
		return sb.toString();
	}

	public String duplicateHash() {
		StringBuilder sb = new StringBuilder();
		sb.append(WaferEvent.class.getName());
		sb.append("(TYPE:").append(this.type.name()).append(")");
		sb.append("(TIME:").append(Long.toString(this.dateAndTime.getTime())).append(")");
		sb.append("(LOT:").append(this.wafer.getLot().getFactoryId()).append(")");
		sb.append("(WAFER:").append(this.wafer.getFactoryId()).append(")");
		sb.append("(PRODUCT:").append(this.product.getPDFId()).append(")");
		sb.append("(OPERATION:").append(this.operation.getFactoryId()).append(")");
		sb.append("(TOOL:").append(this.toolChamber.getParentTool().getFactoryId()).append(")");
		sb.append("(TOOLCHAMBER:").append(this.toolChamber.getFactoryId()).append(")");
		return sb.toString();
	}

	public void setSamplingMethod(SamplingMethod waferSamplingMethod) {
		this.samplingMethod = waferSamplingMethod;
	}

	public String getHashString() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.type.name()).append("_");
		sb.append(this.product.getPDFId()).append("_");
		sb.append(this.operation.getFactoryId()).append("_");
		sb.append(this.wafer.getFactoryId());
		return sb.toString();
	}
	
	@Override
    public boolean equals(Object obj) {
        if (!(obj instanceof WaferEvent)) {
        	return false;
        }
        WaferEvent other = (WaferEvent) obj;
        return this.hashString().equals(other.hashCode());
    }
    
    private String hashString() {
    	StringBuilder sb = new StringBuilder();
		sb.append(this.type.name()).append("_");
		sb.append(this.product.getPDFId()).append("_");
		sb.append(this.operation.getFactoryId()).append("_");
		sb.append(this.wafer.getFactoryId());
		return sb.toString();
    }

    @Override
    public int hashCode() {
		return hashString().hashCode();
    }

	@Override
	public int compareTo(WaferEvent otherWaferEvent) {
		return this.wafer.getSlotNumber().compareTo(otherWaferEvent.wafer.getSlotNumber());
	}

	/**
	 * An enumeration of wafer event types.
	 */
	public enum Type {
		/**
		 * A wafer processing run has begun.
		 */
		BEGIN_RUN,
		/**
		 * A wafer processing run has ended.
		 */
		END_RUN
	}

}
