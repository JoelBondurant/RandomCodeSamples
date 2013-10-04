package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import javax.persistence.*;

/**
 * A class to represent a historical tool prod step (g,s,t) statistics.
 *
 * @author Joel Bondurant.
 * @version 2011.0506
 * @since 1.0
 */
@Entity
@Table(name = "HistToolProdStepStats",
uniqueConstraints =
@UniqueConstraint(columnNames = {"PRODUCT_ID", "TOOL_ID", "STEP_ID", "TEMPORALDATE_ID"}))
@NamedQueries({
	@NamedQuery(name = HistToolProdStepStats.GET_RECORD, query = HistToolProdStepStats.GET_RECORD_QUERY),
	@NamedQuery(name = HistToolProdStepStats.GET_BY_STARTDATE, query = HistToolProdStepStats.GET_BY_STARTDATE_QUERY)
})
public class HistToolProdStepStats implements BaseEntity, Serializable {

	/**
	 * JPA strings.
	 */
	public static final String GET_RECORD = "HistToolProdStepStats.getRecord";
	protected static final String GET_RECORD_QUERY = "select t from HistToolProdStepStats t where t.temporalDate = :aTemporalDate and t.tool = :tool and t.step = :step";
	public static final String GET_BY_STARTDATE = "HistToolProdStepStats.getByStartDate";
	protected static final String GET_BY_STARTDATE_QUERY = "select h from HistToolProdStepStats h where h.temporalDate.dateAndTime >= :startDate";
	public static final String TEMPORALDATE = "temporalDate";
	public static final String SAMPLINGMETHOD = "samplingMethod";
	public static final String STEP = "step";
	public static final String STARTDATE = "startDate";
	/**
	 * Primary Id.
	 */
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;
	/**
	 * Product reference.
	 */
	@ManyToOne(fetch = FetchType.EAGER)
	private Product product;
	/**
	 * Step reference.
	 */
	@ManyToOne(fetch = FetchType.EAGER)
	private Step step;
	/**
	 * Tool reference.
	 */
	@ManyToOne(fetch = FetchType.EAGER)
	private Tool tool;
	/**
	 * TemporalDate reference.
	 */
	@ManyToOne(fetch = FetchType.EAGER)
	private TemporalDate temporalDate;
	/**
	 * n_LotProcCompl
	 */
	@Column(nullable = false)
	private Integer n_LotProcCompl;
	/**
	 * n_LotStepCompl
	 */
	@Column(nullable = false)
	private Integer n_LotStepCompl;
	/**
	 * t_LotProc
	 */
	@Column(nullable = false)
	private Long t_LotProc;
	/**
	 * t_LotCT
	 */
	@Column(nullable = false)
	private Long t_LotCT;

	/**
	 * Default constructor.
	 */
	protected HistToolProdStepStats() {
		this.n_LotProcCompl = 0;
		this.n_LotStepCompl = 0;
		this.t_LotCT = 0L;
		this.t_LotProc = 0L;
	}

	/**
	 * Constructor, all stats are initialized to zero.
	 *
	 * @param product Product.
	 * @param step Step.
	 * @param tool Tool.
	 * @param temporalDate TemporalDate.
	 */
	public HistToolProdStepStats(Product product, Step step, Tool tool, TemporalDate temporalDate) {
		this();
		this.product = product;
		this.step = step;
		this.tool = tool;
		this.temporalDate = temporalDate;
	}

	/**
	 * Product getter.
	 *
	 * @return Product.
	 */
	public Product getProduct() {
		return this.product;
	}

	/**
	 * Step getter.
	 *
	 * @return Step.
	 */
	public Step getStep() {
		return this.step;
	}

	/**
	 * Tool getter.
	 *
	 * @return Tool.
	 */
	public Tool getTool() {
		return this.tool;
	}

	/**
	 * TemporalDate getter.
	 *
	 * @return TemporalDate.
	 */
	public TemporalDate getTemporalDate() {
		return this.temporalDate;
	}

	/**
	 * Increment n_LotProcCompl by one. (n_LotProcCompl++)
	 *
	 * @return this.
	 */
	public HistToolProdStepStats incrementNumLotProcessingComplete() {
		this.n_LotProcCompl += 1;
		return this;
	}

	/**
	 * Increment n_LotStepCompl by one. (n_LotStepCompl++)
	 *
	 * @return this.
	 */
	public HistToolProdStepStats incrementNumLotStepComplete() {
		this.n_LotStepCompl += 1;
		return this;
	}

	/**
	 * Add time to t_LotProc.
	 *
	 * @param timeDifferenceInSeconds Number of seconds to add.
	 * @return this.
	 */
	public HistToolProdStepStats addLotProcTime(Long timeDifferenceInSeconds) {
		this.t_LotProc += timeDifferenceInSeconds;
		return this;
	}

	/**
	 * Add time to t_LotCT.
	 *
	 * @param timeDifferenceInSeconds Number of seconds to add.
	 * @return this.
	 */
	public HistToolProdStepStats addLotCycleTime(Long timeDifferenceInSeconds) {
		this.t_LotCT += timeDifferenceInSeconds;
		return this;
	}

	/**
	 * Map key generator.
	 *
	 * @param prd Product.
	 * @param st Step.
	 * @param tl Tool.
	 * @param td TemporalDate.
	 * @return mapKey.
	 */
	public static String generateMapKey(Product prd, Step st, Tool tl, TemporalDate td) {
		StringBuilder sb = new StringBuilder();
		sb.append(prd.getId()).append("_");
		sb.append(st.getId()).append("_");
		sb.append(tl.getId()).append("_");
		sb.append(td.getId());
		return sb.toString();
	}
	
	private String mapKey;
	
	public synchronized void generateMapKey() {
		this.mapKey = generateMapKey(this.product, this.step, this.tool, this.temporalDate);
	}

	public String getMapKey() {
		if (this.mapKey == null) {
			generateMapKey();
		}
		return this.mapKey;
	}

	@Override
	public Long getId() {
		return this.id;
	}
}
