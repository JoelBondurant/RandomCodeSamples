classdef Database < handle

	properties (SetAccess = private, GetAccess = public)
		NUMERIC = 'numeric';
		MIXED = 'cellarray';
	end
	
	properties (SetAccess = private, GetAccess = public)
		databaseName = 'imDev';
		userName = 'REMOVED';
		password = 'REMOVED';
		driver = 'com.microsoft.sqlserver.jdbc.SQLServerDriver';
		server = 'SASERVER1';
		instance = 'SQL2008R2';
		portNumber = '1433';
		batchSize = 10000;
		databaseUrl;
		dbConn;
	end
	
	methods
		function obj = Database(databaseName)
			if (nargin > 0)
				obj.databaseName = databaseName;
			end
			obj.databaseUrl = ['jdbc:sqlserver://',obj.server,'\',obj.instance,':',obj.portNumber,';databaseName=',obj.databaseName,';integratedSecurity=false;'];
			obj.dbConn = database(obj.databaseName, obj.userName, obj.password, obj.driver, obj.databaseUrl);
			setdbprefs('DataReturnFormat', 'numeric');
			setdbprefs('ErrorHandling', 'empty');
		end
		
		function obj = setDataReturnFormat(obj, format)
			setdbprefs('DataReturnFormat', format);
		end
		
		function data = query(obj, query)
			data = fetch(obj.dbConn, query);
		end
		
		function close(obj)
			close(obj.dbConn);
		end
		
		function exec(obj, query)
			exec(obj.dbConn, query);
		end
		
		function dbName = getDbName(obj)
			dbName = obj.databaseName;
		end
		
		function insert(obj, tableName, colNames, values)
			writeToLog(strcat('Database insert begin: (', tableName, ').'));
			lenVals = size(values, 1);
			numBatches = floor(lenVals / obj.batchSize);
			m = 0;
			for batch = 1:numBatches
				n = obj.batchSize * (batch - 1) + 1;
				m = n + obj.batchSize - 1;
				datainsert(obj.dbConn, tableName, colNames, values(n:m, :));
			end
			if ((m + 1) <= lenVals)
				datainsert(obj.dbConn, tableName, colNames, values((m + 1):lenVals, :));
			end
			writeToLog(strcat('Database insert end: (', num2str(lenVals), ') values written.'));
		end
		
		function oldInsert(obj, tableName, colNames, values)
			writeToLog(strcat('Database insert begin: (', tableName, ').'));
			lenVals = size(values, 1);
			numBatches = floor(lenVals / obj.batchSize);
			m = 0;
			for batch = 1:numBatches
				n = obj.batchSize * (batch - 1) + 1;
				m = n + obj.batchSize - 1;
				fastinsert(obj.dbConn, tableName, colNames, values(n:m, :));
			end
			if ((m + 1) <= lenVals)
				fastinsert(obj.dbConn, tableName, colNames, values((m + 1):lenVals, :));
			end
			writeToLog(strcat('Database insert end: (', num2str(lenVals), ') values written.'));
		end
		
		function bulkInsert(obj, tableName, fileName)
			writeToLog(strcat('Bulk database insert begin: (', tableName, ').'));
			query = ['BULK INSERT [',tableName,'] ',...
					'FROM ''', fileName, ''' ',...
					'WITH ( FIELDTERMINATOR = ''\t'', ROWTERMINATOR = ''\n'', ',...
					'FORMATFILE = ''C:/SensorAnalytics/trunk/SQL/FormatFiles/', tableName, '.fmt'' );'];
			obj.exec(query);
			writeToLog(strcat('Bulk database insert end.'));
		end
		
		function prepare1234paradigm(obj)
			prepProducts = ['SELECT ProductId, ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY ProductFamilyId, DeviceId, ProductId) AS MatProductId ',...
				'INTO #MatProductMap FROM ProductView;'];
			obj.exec(prepProducts);

			prepTools = ['SELECT ToolId, ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY ToolTypeId, ToolSubTypeId, ToolId) AS MatToolId ',...
				'INTO #MatToolMap FROM ToolView;'];
			obj.exec(prepTools);

			prepSamplingMethods = ['SELECT Id AS SamplingMethodId, ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY IsDefault DESC, Id ASC) AS MatSamplingMethodId ',...
				'INTO #MatSamplingMethodMap FROM SamplingMethod WITH (NOLOCK); select 1;'];
			obj.exec(prepSamplingMethods);
			
			prepSamplingMethods = ['SELECT Id AS ToolStateId, ROW_NUMBER() OVER (PARTITION BY 1 ORDER BY Id ASC) AS MatToolStateId ',...
				'INTO #MatToolStateMap FROM ToolState WITH (NOLOCK);'];
			obj.exec(prepSamplingMethods);
		end
		
		function deploy(obj)
			deploymentScriptPath = 'C:/SensorAnalytics/trunk/Deployment';
			deploymentScript = 'deploySQL.py';
			deployCmd = ['python',' ',deploymentScriptPath,'/',deploymentScript,' ',deploymentScriptPath,' ',obj.server,' ',obj.databaseName,' ',obj.userName,' ',obj.password];
			system(deployCmd);
			system(deployCmd);
		end
		
	end

end

