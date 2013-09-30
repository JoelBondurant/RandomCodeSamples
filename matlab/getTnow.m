function [tNow] = getTnow(db, processBatchId)

	%% Get the core data from the datasource.
	query = ['select tNow from ProcessBatch with (nolock) where id = ',num2str(processBatchId)];
	db.setDataReturnFormat('cellarray');
	y = db.query(query);
	tNow = DateTime(y);
	
end

