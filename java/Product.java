package com.sensoranalytics.inspectionmanager.entity;

import java.io.Serializable;
import javax.persistence.*;

/**
 * A class to represent a factory product.
 *
 * @author Joel Bondurant.
 * @version 2011.0321
 * @since 1.0
 */
@Entity
public class Product implements FactoryEntity, Serializable {

	public static final String PDF_ID_DELIMITER = "_";
	public static final String PROD = "PROD";
	public static final String QUAL = "QUAL";
	public static final String OTHER = "OTHER";


	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	private Long id;
	@Column(length = 50, nullable = false)
	private String factoryId;
	@Column(length = 50, nullable = true)
	private String useCode;
	@Column(nullable = false)
	private Long fileImportId;
	@OneToOne(mappedBy = "product", fetch = FetchType.EAGER, cascade = CascadeType.ALL)
	private Flow flow;
	@ManyToOne(fetch = FetchType.LAZY, cascade = CascadeType.PERSIST)
	private Device device;

	protected Product() {
		this.flow = new Flow(this);
	}

	/**
	 * Constructor.
	 *
	 * @param factoryId A unique identifier for the product.
	 * @param useCode A description of the product's use.
	 * @param device The product device classification for the product.
	 * @param fileImportId A link to the file import which created the product.
	 */
	public Product(String factoryId, String useCode, Device device, Long fileImportId) {
		this();
		this.factoryId = factoryId;
		this.useCode = useCode;
		this.device = device;
		this.fileImportId = fileImportId;
	}

	/**
	 * Flow getter.
	 *
	 * @return The flow for the product.
	 */
	public Flow getFlow() {
		return this.flow;
	}

	@Override
	public String getFactoryId() {
		return this.factoryId;
	}

	/**
	 * Use description getter.
	 *
	 * @return The use-description for the product.
	 */
	public String getUseCode() {
		return this.useCode;
	}

	/**
	 * Use description setter.
	 *
	 * @param useDescription The use description for the product.
	 * @return this.
	 */
	public Product setUseCode(String useCode) {
		this.useCode = useCode;
		return this;
	}

	/**
	 * Device getter.
	 *
	 * @return The product device to which this product belongs.
	 */
	public Device getDevice() {
		return this.device;
	}

	@Override
	public Long getId() {
		return this.id;
	}

	public String getPDFId() {
		StringBuilder sb = new StringBuilder();
		sb.append(this.getFactoryId()).append(PDF_ID_DELIMITER);
		sb.append(this.getDevice().getFactoryId()).append(PDF_ID_DELIMITER);
		sb.append(this.getDevice().getProductFamily().getFactoryId());
		return sb.toString();
	}

	public boolean isProd() {
		return this.useCode.equals(PROD);
	}

	public boolean isQual() {
		return this.useCode.equals(QUAL);
	}

	public boolean isOther() {
		return this.useCode.equals(OTHER);
	}
	
	@Override
    public boolean equals(Object obj) {
        if (!(obj instanceof Product)) {
        	return false;
        }
        Product other = (Product) obj;
        return this.getPDFId().equals(other.getPDFId());
    }

    @Override
    public int hashCode() {
		return this.getPDFId().hashCode();
    }
}
