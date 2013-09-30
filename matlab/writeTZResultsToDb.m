function writeTZResultsToDb(db, facDims, ctq)
	
	writeToLog('writeTZResultsToDb: begin.');
	processBatchId = facDims.processBatchId;
	id_t = facDims.id_t;
	id_z = facDims.id_z;
	f_InState_tz = ctq.f_InState_tz;
	t_InStateAve_tz = ctq.t_InStateAve_tz;
	
	numRows = 0;
	for t = 1:length(f_InState_tz.t)
		for z = 1:1:length(f_InState_tz.t(t).z)
			numRows = numRows + 1;
		end
	end

	colNames = {'PROCESSBATCH_ID','TOOL_ID','TOOLSTATE_ID','f_InState','t_InStateAve'};
	resultsTZ = NaN(numRows, length(colNames));
	
	i = 0;
	for t = 1:length(f_InState_tz.t)
		for z = 1:1:length(f_InState_tz.t(t).z)
			i = i + 1;
			tid = id_t(t);
			zid = id_z(z);
			resultsTZ(i, 1) = processBatchId;
			resultsTZ(i, 2) = tid;
			resultsTZ(i, 3) = zid;
			resultsTZ(i, 4) = f_InState_tz.t(t).z(z);
			resultsTZ(i, 5) = 3600 * t_InStateAve_tz.t(t).z(z);
		end
	end
	
	db.insert('ResultsTZ', colNames, resultsTZ);
	writeToLog('writeTZResultsToDb: end.');
end

