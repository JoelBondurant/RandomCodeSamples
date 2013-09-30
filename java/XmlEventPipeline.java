package com.sensoranalytics.inspectionmanager.fileimport;



/**
 * Pipeline for event xml process.
 * @author Joel Bondurant
 * @version 2011.1023
 * @since 1.0.0
 */
public class XmlEventPipeline {

	public static final String PIPELINE_NAME = "EventXML";
	public static final String FILENAME_REGEX = "^events\\d{8}T\\d{6}(\\(\\d+\\))?\\.xml$";
	public static final String DESCRIPTION = "Factory xml event information.";
	public static final int LengthOfFileNamePrefix = 6; // length of "events"

}
