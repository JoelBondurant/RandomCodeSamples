function [S_StepToTools_gs] = getProductStepTools(db, S_Products, S)
	
	%% Get the core data from the datasource.
	query = ['SELECT pm.MatProductId, tm.MatToolId, pfv.StepNumber ', ...
		'FROM ProductFlowView pfv ', ...
		'JOIN #MatProductMap pm ON (pm.ProductId = pfv.ProductId) ', ...
		'JOIN Recipe r with (nolock) ', ...
		'ON (pfv.productid = r.product_id AND pfv.operationid = r.operation_id) ', ...
		'JOIN #MatToolMap tm ON (r.tool_id = tm.ToolId) ', ...
		'ORDER BY 1 ASC, 2 ASC, 3 ASC; '];
	db.setDataReturnFormat('numeric');
	y = db.query(query);
	
	G = length(S_Products);
	S_StepToTools_gs = cell(G, S);

	for n = 1:length(y)
		g = y(n, 1);
		t = y(n, 2);
		s = y(n, 3);
		S_StepToTools_gs{g, s}(length(S_StepToTools_gs{g, s}) + 1) = t;
	end
	
end

