function [t_CTAve_gs] = getCtAve(facDims, options)
	
	t_LotCT_gstp = facDims.t_LotCT_gstp;
	n_LotStepCompl_gstp = facDims.n_LotStepCompl_gstp;
	
	% IMInp1500
	for g = facDims.S_Products
		for s = facDims.S_Steps_g{g}
			temp1 = 0;
			temp2 = 0;
			for t = facDims.S_StepToTools_gs{g, s}
				for p = 1:options.n_PerInHorz
					temp1 = temp1 + t_LotCT_gstp.g(g).s(s).t(t).p(p);
					temp2 = temp2 + n_LotStepCompl_gstp.g(g).s(s).t(t).p(p);
				end
			end
			if (temp2 > 0)
				t_CTAve_gs.g(g).s(s) = temp1 / temp2;
			else
				t_CTAve_gs.g(g).s(s) = 0;
			end
		end
	end
	clear temp;
	
	% Fill100
	S_EmptySteps_gtSTY = cell(facDims.G, facDims.TSTY);
	S_FullSteps_gtSTY = cell(facDims.G, facDims.TSTY);
	S_EmptyProds = [];
	for g = facDims.S_Products
		for tSTY = facDims.S_ToolSubTypes
			for s = facDims.S_Steps_gtSTY{g, tSTY}
				if (t_CTAve_gs.g(g).s(s) == 0)
					S_EmptySteps_gtSTY{g, tSTY} = [S_EmptySteps_gtSTY{g, tSTY}, s];
				end
			end
			S_FullSteps_gtSTY{g, tSTY} = setdiff(facDims.S_Steps_gtSTY{g, tSTY}, S_EmptySteps_gtSTY{g, tSTY});
			if ~isempty(S_EmptySteps_gtSTY{g, tSTY})
				S_EmptyProds = unique([S_EmptyProds, g]);
			end
		end
	end
	
	if isempty(S_EmptyProds)
		return; % We're done messing with the return results.
	end
	
	% Fill200
	n_CTValues_gtSTY = zeros(facDims.G, facDims.TSTY);
	t_CTEst_gtSTY = zeros(facDims.G, facDims.TSTY);
	for g = facDims.S_Products
		for tSTY = facDims.S_ToolSubTypes
			temp = length(S_FullSteps_gtSTY{g, tSTY});
			if (temp ~= 0)
				n_CTValues_gtSTY(g, tSTY) = temp;
				temp2 = 0;
				for s = S_FullSteps_gtSTY{g, tSTY}
					temp2 = temp2 + t_CTAve_gs.g(g).s(s);
				end
				t_CTEst_gtSTY(g, tSTY) = (1 / temp) * temp2;
			end
		end
	end
	clear temp temp2;
	
	% Fill300
	n_CTValues_tSTY = zeros(facDims.TSTY, 1);
	t_CTEst_tSTY = zeros(facDims.TSTY, 1);
	for tSTY = facDims.S_ToolSubTypes
		temp = sum(n_CTValues_gtSTY(:, tSTY));
		if (temp ~= 0)
			n_CTValues_tSTY(tSTY) = temp;
			temp2 = 0;
			for g = facDims.S_Products
				temp2 = temp2 + (n_CTValues_gtSTY(g, tSTY) * t_CTEst_gtSTY(g, tSTY));
			end
			t_CTEst_tSTY(tSTY) = (1 / temp) * temp2;
		end
	end
	clear temp temp2;
	
	% Fill400
	n_CTValues = sum(n_CTValues_tSTY);
	if (n_CTValues ~= 0)
		temp = 0;
		for tSTY = facDims.S_ToolSubTypes
			temp = temp + (n_CTValues_tSTY(tSTY) * t_CTEst_tSTY(tSTY));
		end
		t_CTEst = (1 / n_CTValues) * temp;
	else
		t_CTEst = 0;
	end
	
	% Fill500
	for g = S_EmptyProds
		for tSTY = facDims.S_ToolSubTypes
			if (n_CTValues_gtSTY(g, tSTY) > 0)
				for s = S_EmptySteps_gtSTY{g, tSTY}
					t_CTAve_gs.g(g).s(s) = t_CTEst_gtSTY(g, tSTY);
				end
			elseif (n_CTValues_tSTY(tSTY) > 0)
				for s = S_EmptySteps_gtSTY{g, tSTY}
					t_CTAve_gs.g(g).s(s) = t_CTEst_tSTY(tSTY);
				end
			elseif (n_CTValues > 0)
				for s = S_EmptySteps_gtSTY{g, tSTY}
					t_CTAve_gs.g(g).s(s) = t_CTEst;
				end
			else
				ex = MException('t_CTAve_gs:NotFilled', 'Not enough data to estimate t_CTAve_gs.');
				throw(ex);
			end
		end
	end

end

