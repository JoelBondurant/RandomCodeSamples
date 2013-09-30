# select * from natsemiraw..eventxml order by transdate asc; -> events.txt, eventHeaders.txt
import time, datetime


def makeEvents(fileName, startDate, endDate):
	print("Making event file: " + fileName)
	#################################### Wafer Sampling Data ####################################
	defectDataFile = open('C:/SensorAnalytics/trunk/FactoryData/NatSemi/095-DefectData/020-Merge/merged.txt', 'rt')
	waferSamplingMap = {}
	for txtLine in defectDataFile:
		txtLineSplit = txtLine.split('\t')
		lotId = txtLineSplit[0]
		waferNumber = int(txtLineSplit[1])
		if lotId not in waferSamplingMap:
			waferSamplingMap[lotId] = set()
		waferSamplingMap[lotId].add(waferNumber)
	defectDataFile.close()
	
	######################################### Tool Data #########################################
	facDimFile = open('C:/SensorAnalytics/trunk/FactoryData/NatSemi/080-FacDims/factoryDimensions20120716T000000.txt', 'rt')
	toolMap = {}
	for txtLine in facDimFile:
		txtLineSplit = txtLine.split('\t')
		if (txtLineSplit[0] == 'TL'):
			toolId = txtLineSplit[1]
			toolTypeId = txtLineSplit[2]
			toolSubTypeId = txtLineSplit[3]
			toolMap[toolId] = [toolTypeId, toolSubTypeId]
	
	facDimFile.close()
	
	################################### Lot Event XML Product ###################################
	
	eventFile = open("C:/SensorAnalytics/trunk/FactoryData/NatSemi/090-EventXML/events.txt", "rt")
	
	eventsHeader = '<?xml version="1.0"?>\n<Events xmlns="http://www.sensoranalytics.com" '
	eventsHeader += 'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.sensoranalytics.com events.xsd">\n'
	eventsFooter = "</Events>\n"
	
	eventXMLFile = open(fileName, "wt")
	eventXMLFile.write(eventsHeader)
	
	toolChamberId = "TC-1"
	
	for eventLine in eventFile:
		eventTxt = eventLine.replace("\n", "")
		eventData = eventTxt.split("\t")
		eventDataMap = {}
		eventDataMap["Event"] = eventData[0]
		lotId = eventData[1]
		eventDataMap["Lot"] = lotId
		transDateStr = eventData[2]
		eventDataMap["TransDate"] = transDateStr
		transDate = datetime.datetime.strptime(transDateStr, '%Y-%m-%dT%H:%M:%S.%f')
		if not (startDate <= transDate < endDate):
			continue
		eventDataMap["NumWafers"] = eventData[3]
		eventDataMap["Tool"] = eventData[4]
		eventDataMap["ToolSubType"] = eventData[5]
		eventDataMap["ToolType"] = eventData[6]
		eventDataMap["Operation"] = eventData[7]
		eventDataMap["ProdUse"] = eventData[8]
		eventDataMap["Product"] = eventData[9]
		eventDataMap["Device"] = eventData[10]
		eventDataMap["Family"] = eventData[11]
		eventDataMap["NextTool"] = eventData[12]
		eventDataMap["NextOperation"] = eventData[13]
		eventDataMap["NextProduct"] = eventData[14]
		eventDataMap["NextDevice"] = eventData[15]
		eventDataMap["NextFamily"] = eventData[16]
		eventDataMap["RecipeId"] = eventData[17]
		eventDataMap["OldE10State"] = eventData[18]
		eventDataMap["NewE10State"] = eventData[19]
		eventDataMap["Id"] = eventData[20]
		# write xml
		eventXMLFile.write("<LotEvent>\n")
		eventXMLFile.write("\t<Type>" + eventDataMap["Event"] + "</Type>\n")
		eventXMLFile.write("\t<LotId>" + eventDataMap["Lot"] + "</LotId>\n")
		eventXMLFile.write("\t<ToolId>" + eventDataMap["Tool"] + "</ToolId>\n")
		eventXMLFile.write("\t<NextToolId>" + eventDataMap["NextTool"] + "</NextToolId>\n")
		eventXMLFile.write("\t<DateTime>" + eventDataMap["TransDate"] + "</DateTime>\n")
		eventXMLFile.write("\t<WaferEvents>\n")
		if lotId in waferSamplingMap:
			getsProcessed = waferSamplingMap[lotId]
		else:
			getsProcessed = set()
		numWafers = int(eventDataMap["NumWafers"])
		for waferNumber in range(1, numWafers + 1):
			eventXMLFile.write("\t\t<WaferEvent>\n")
			eventXMLFile.write("\t\t\t<WaferId>WAF-" + str(waferNumber) + "</WaferId>\n")
			eventXMLFile.write("\t\t\t<Slot>" + str(waferNumber) + "</Slot>\n")
			eventXMLFile.write("\t\t\t<OperationId>" + eventDataMap["Operation"] + "</OperationId>\n")
			eventXMLFile.write("\t\t\t<ToolChamberId>" + toolChamberId + "</ToolChamberId>\n")
			eventXMLFile.write("\t\t\t<UseCode>" + eventDataMap["ProdUse"] + "</UseCode>\n")
			eventXMLFile.write("\t\t\t<ProductId>" + eventDataMap["Product"] + "</ProductId>\n")
			eventXMLFile.write("\t\t\t<DeviceId>" + eventDataMap["Device"] + "</DeviceId>\n")
			eventXMLFile.write("\t\t\t<ProductFamilyId>" + eventDataMap["Family"] + "</ProductFamilyId>\n")
			eventXMLFile.write("\t\t\t<NextOperationId>" + eventDataMap["NextOperation"] + "</NextOperationId>\n")
			eventXMLFile.write("\t\t\t<NextProductId>" + eventDataMap["NextProduct"] + "</NextProductId>\n")
			eventXMLFile.write("\t\t\t<NextDeviceId>" + eventDataMap["NextDevice"] + "</NextDeviceId>\n")
			eventXMLFile.write("\t\t\t<NextProductFamilyId>" + eventDataMap["NextFamily"] + "</NextProductFamilyId>\n")
			eventXMLFile.write("\t\t\t<RecipeId>" + eventDataMap["RecipeId"] + "</RecipeId>\n")
			eventXMLFile.write("\t\t\t<TagIds></TagIds>\n")
			eventXMLFile.write("\t\t\t<GetsProcessed>")
			if (eventDataMap["Event"] == 'BEGR'):
				if (eventDataMap["Tool"] not in toolMap):
					eventXMLFile.write("1")
				elif (toolMap[eventDataMap["Tool"]][0] == 'INSP'):
					if (toolMap[eventDataMap["Tool"]][1] == 'Macro'):
						eventXMLFile.write("1")
					else:
						if (waferNumber in getsProcessed):
							eventXMLFile.write("1")
						else:
							eventXMLFile.write("0")
				else:
					eventXMLFile.write("1")
			else:
				if (eventDataMap["NextTool"] not in toolMap):
					eventXMLFile.write("1")
				elif (toolMap[eventDataMap["NextTool"]][0] == 'INSP'):
					if (toolMap[eventDataMap["NextTool"]][1] == 'Macro'):
						eventXMLFile.write("1")
					else:
						if (waferNumber in getsProcessed):
							eventXMLFile.write("1")
						else:
							eventXMLFile.write("0")
				else:
					eventXMLFile.write("1")
			eventXMLFile.write("</GetsProcessed>\n")
			eventXMLFile.write("\t\t</WaferEvent>\n")
		eventXMLFile.write("\t</WaferEvents>\n")
		eventXMLFile.write("</LotEvent>\n")
		eventXMLFile.write("<ToolEvent>\n")
		eventXMLFile.write("\t<ToolId>" + eventDataMap["Tool"] + "</ToolId>\n")
		eventXMLFile.write("\t<DateTime>" + eventDataMap["TransDate"] + "</DateTime>\n")
		eventXMLFile.write("\t<OldToolState>" + eventDataMap["OldE10State"] + "</OldToolState>\n")
		eventXMLFile.write("\t<NewToolState>" + eventDataMap["NewE10State"] + "</NewToolState>\n")
		eventXMLFile.write("\t<ToolChamberEvents>\n")
		eventXMLFile.write("\t\t<ToolChamberEvent>\n")
		eventXMLFile.write("\t\t\t<ToolChamberId>" + toolChamberId + "</ToolChamberId>\n")
		eventXMLFile.write("\t\t\t<OldToolChamberState>" + eventDataMap["OldE10State"] + "</OldToolChamberState>\n")
		eventXMLFile.write("\t\t\t<NewToolChamberState>" + eventDataMap["NewE10State"] + "</NewToolChamberState>\n")
		eventXMLFile.write("\t\t</ToolChamberEvent>\n")
		eventXMLFile.write("\t</ToolChamberEvents>\n")
		eventXMLFile.write("</ToolEvent>\n")
		
	eventFile.close()
	eventXMLFile.write(eventsFooter)
	eventXMLFile.close()
	print(fileName + " written.")

