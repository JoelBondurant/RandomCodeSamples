import datetime, re

class WaferMeasurementEvent:
	def __init__(self, waferId, area, pid):
		self.waferId = waferId
		self.area = area
		self.pid = pid
	def mapKey(self):
		return self.waferId
	def xml(self):
		xml = '\t\t<WaferMeasurementEvent>\n\t\t\t<WaferId>'
		xml += self.waferId + '</WaferId>\n\t\t\t<AreaInspected>' + str(float(self.area)) + '</AreaInspected>\n\t\t\t'
		xml += '<Metric>\n\t\t\t\t<MetricId>PID</MetricId>\n\t\t\t\t<ControlChartId>A</ControlChartId>\n\t\t\t\t'
		xml += '<Type>COUNT</Type>\n\t\t\t\t<Value>' + str(float(self.pid)) + '</Value>\n\t\t\t\t'
		xml += '<ReviewFraction>0.0</ReviewFraction>\n\t\t\t</Metric>\n\t\t</WaferMeasurementEvent>\n'
		return xml

class LotMeasurementEvent:
	def __init__(self, lotId, finishTime, toolId):
		self.lotId = lotId
		self.finishTime = finishTime
		self.toolId = toolId
		self.waferMeasurementEvents = {}
	def matches(self, other):
		return (self.lotId == other.lotId and self.finishTime == other.finishTime and self.toolId == other.toolId)
	def mapKey(self):
		return (self.lotId + self.finishTime + self.toolId)
	def addWaferMeasurementEvent(self, waferMeasurementEvent):
		self.waferMeasurementEvents[waferMeasurementEvent.mapKey()] = waferMeasurementEvent
	def xml(self):
		xml = '<LotMeasurementEvent>\n\t<Type>DEFECT</Type>\n\t<LotId>' + self.lotId + '</LotId>\n\t<ToolId>'
		xml += self.toolId + '</ToolId>\n\t<DateTime>' + self.finishTime + '</DateTime>\n\t<WaferMeasurementEvents>\n'
		pids = []
		for waferMeasurementEvent in self.waferMeasurementEvents.values():
			xml += waferMeasurementEvent.xml()
			pid = int(waferMeasurementEvent.pid)
			pids.append(pid)
		CLValue = float(sum(pids))/float(len(pids))
		xml += '\t</WaferMeasurementEvents>\n\t<ControlCharts>\n\t\t<ControlChart>\n\t\t\t<ControlChartId>A'
		xml += '</ControlChartId>\n\t\t\t<Type>X_BAR</Type>\n\t\t\t<CL>' + str(CLValue) + '</CL>\n\t\t\t'
		xml += '<UCL>'+str(2.0*CLValue)+'</UCL>\n\t\t\t<UCLSigma>2.7</UCLSigma>\n\t\t\t<LCL>0.0</LCL>\n\t\t'
		xml += '</ControlChart>\n\t</ControlCharts>\n</LotMeasurementEvent>\n'
		return xml

def makeEvents(fileName, startDate, endDate):
	print("Making event file: " + fileName)
	# Map defect data into memory model from text file.
	lotMeasurementEvents = {}
	defectDataFile = open('C:/SensorAnalytics/trunk/FactoryData/NatSemi/095-DefectData/020-Merge/merged.txt', 'rt')
	for textLine in defectDataFile:
		textLineSplit = textLine.split('\t')
		lotId = textLineSplit[0]
		waferId = 'WAF-' + textLineSplit[1]
		finishTime = textLineSplit[2]
		eventTime = datetime.datetime.strptime(finishTime, '%Y-%m-%dT%H:%M:%S')
		if not (startDate <= eventTime < endDate):
			continue
		toolId = textLineSplit[3]
		toolId = re.sub('-.+', '', toolId) # needed to pull off -B and -PM1 additions in defect tool names.
		area = textLineSplit[4]
		pid = textLineSplit[5][:-1]
		lotMeasurementEvent = LotMeasurementEvent(lotId, finishTime, toolId)
		if (lotMeasurementEvent.mapKey() in lotMeasurementEvents):
			lotMeasurementEvent = lotMeasurementEvents[lotMeasurementEvent.mapKey()]
		else:
			lotMeasurementEvents[lotMeasurementEvent.mapKey()] = lotMeasurementEvent
		waferMeasurementEvent = WaferMeasurementEvent(waferId, area, pid)
		lotMeasurementEvent.addWaferMeasurementEvent(waferMeasurementEvent)
	defectDataFile.close()
	
	eventsHeader = '<?xml version="1.0"?>\n<Events xmlns="http://www.sensoranalytics.com" '
	eventsHeader += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sensoranalytics.com events.xsd">\n'
	
	xmlFile = open(fileName, 'wt')
	xmlFile.write(eventsHeader)
	for lotMeasurementEvent in lotMeasurementEvents.values():
		xmlFile.write(lotMeasurementEvent.xml())
	xmlFile.write('</Events>')
	xmlFile.close()
	print(fileName + ' written.')

