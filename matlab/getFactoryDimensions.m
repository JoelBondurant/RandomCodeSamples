function [G, S, T] = getFactoryDimensions(db)
	
	%% Get the core data from the datasource.
	query = 'select count(distinct productid) as G, max(stepnumber) as S from ProductFlowView;';
	db.setDataReturnFormat('numeric');
	y = db.query(query);
	
	G = y(1);
	S = y(2);
	
	query = 'select count(1) as T from ToolView;';
	T = db.query(query);
	
end

