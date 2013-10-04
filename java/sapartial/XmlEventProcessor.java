package com.sensoranalytics.inspectionmanager.fileimport;

import com.sensoranalytics.inspectionmanager.entity.FileImport;
import com.sensoranalytics.inspectionmanager.entity.LotEvent;
import com.sensoranalytics.inspectionmanager.entity.LotMeasurementEvent;
import com.sensoranalytics.inspectionmanager.entity.ToolEvent;
import com.sensoranalytics.inspectionmanager.facade.LotFacadeLocal;
import com.sensoranalytics.inspectionmanager.jaxb.Events;
import com.sensoranalytics.inspectionmanager.jaxb.ObjectFactory;
import com.sensoranalytics.logging.LogHandler;
import com.sensoranalytics.logging.LoggerFactory;
import java.util.List;
import java.util.logging.Logger;
import javax.ejb.EJB;
import javax.ejb.Stateless;


/**
 * Class which processes XML event files and persists the to storage.
 * @author Joel Bondurant
 */
@Stateless
public class XmlEventProcessor {

	private static final Logger logger = LoggerFactory.getLogger(FileProcessor.LOG_ZONE);
	@EJB private FactoryFacadeLocal factoryFacade;
	@EJB private LotFacadeLocal lotFacade;

	public boolean digest(FileImport fileImport) {
		Factory factory = new Factory();
		factoryFacade.fillForEventProcessing(factory);
		logger.info("File event parsing under way.");
		try {
			javax.xml.bind.JAXBContext jaxbCtx = javax.xml.bind.JAXBContext.newInstance(ObjectFactory.class);
			javax.xml.bind.Unmarshaller unmarshaller = jaxbCtx.createUnmarshaller();
			Events evts = (Events) unmarshaller.unmarshal(fileImport.getFile());
			List<Object> eventGroup = evts.getEventGroup();
			for (Object evt: eventGroup) {
				if (evt instanceof Events.LotEvent) {
					Events.LotEvent lotEvent = (Events.LotEvent) evt;
					try {
						LotEvent lotEventEntity = LotEventBuilder.build(lotEvent, lotFacade, factory, fileImport.getId());
						factory.putLotEvent(lotEventEntity);
					} catch (Exception ex) {
						logger.severe(ex.toString());
						logger.severe(LogHandler.stackTrace(ex));
					}
				}
			}
			for (Object evt: eventGroup) {
				if (evt instanceof Events.ToolEvent) {
					Events.ToolEvent toolEvent = (Events.ToolEvent) evt;
					try {
						ToolEvent toolEventEntity = ToolEventBuilder.build(toolEvent, factory, fileImport.getId());
						factory.putToolEvent(toolEventEntity);
					} catch (Exception ex) {
						logger.severe(ex.toString());
						logger.severe(LogHandler.stackTrace(ex));
					}
				}
			}
			for (Object evt: eventGroup) {
				if (evt instanceof Events.LotMeasurementEvent) {
					Events.LotMeasurementEvent lotMeasurementEvent = (Events.LotMeasurementEvent) evt;
					try {
						LotMeasurementEvent lotMeasurementEventEntity = LotMeasurementEventBuilder.build(lotMeasurementEvent, lotFacade, factory, fileImport.getId());
						factory.putLotMeasurementEvent(lotMeasurementEventEntity);
					} catch (Exception ex) {
						logger.severe(ex.toString());
						logger.severe(LogHandler.stackTrace(ex));
					}
				}
			}
			factoryFacade.commit(factory);
		} catch (Exception ex) {
			logger.severe(ex.toString());
			logger.severe(LogHandler.stackTrace(ex));
			return false;
		}
		return true;
	}

}
