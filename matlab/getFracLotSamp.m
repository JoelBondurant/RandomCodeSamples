function [f_LotSamp_gssSA] = getFracLotSamp(db, tTY_id, tTY_Name, S_Products, S_Steps_g, S_SamplingMethods)

% IMInp1700

query = ['select a.MatProductId, a.StepNumber, isnull(b.MatSamplingMethodId, -2) as MatSamplingMethodId, ',...
	'a.ToolTypeId, b.Interval ',...
	'from ( ',...
	'select pm.MatProductId, pfv.ProductId, pfv.StepNumber, op.ToolType_Id as ToolTypeId ',...
	'from ProductFlowView pfv ',...
	'join #MatProductMap pm on (pfv.ProductId = pm.ProductId) ',...
	'join Operation op with (nolock) ',...
	'on (pfv.OperationId = op.id) ',...
	') a ',...
	'left join ',...
	'( ',...
	'select distinct pfv.ProductId, pfv.StepNumber, ',...
	'isnull(sm.id, -1) as SamplingMethodId, isnull(smm.MatSamplingMethodId, -1) as MatSamplingMethodId, ',...
	'irule.LongParameterOne as Interval ',...
	'from SamplingRecord sam with (nolock) ',...
	'join InspectionRule irule with (nolock) on (sam.lotsamplingrule_id = irule.id) ',...
	'join ProductFlowView pfv on (sam.step_id = pfv.StepId) ',...
	'left join Tag t with (nolock) on (sam.tagonoperation_id = t.id) ',...
	'left join SamplingMethod_Tag smt with (nolock) on (smt.tags_id = t.id) ',...
	'left join SamplingMethod sm with (nolock) on (sm.id = smt.samplingmethod_id and sm.iscombo = 0) ',...
	'left join #MatSamplingMethodMap smm on (sm.id = smm.samplingmethodid) ',...
	') b ',...
	'on (a.productid = b.productid and a.stepnumber = b.stepnumber);'];
db.setDataReturnFormat('numeric');
y = db.query(query);
dataLength = size(y, 1);

% initalize to zero.
for g = S_Products
	for s = S_Steps_g{g}
		for sSA = S_SamplingMethods
			f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = 0.0;
		end
	end
end


% figure out if a default sam record exists for (g, s).
for i = 1:dataLength
	g = y(i, 1);
	s = y(i, 2);
	hasDefaultSAMRecord.g(g).s(s) = 0;
	hasNonDefaultSAMRecord.g(g).s(s) = 0;
end
for i = 1:dataLength
	g = y(i, 1);
	s = y(i, 2);
	if (y(i, 3) == -1)
		sSA = 1;
	elseif (y(i, 3) == -2)
		sSA = NaN;
	else
		sSA = y(i, 3);
	end
	if (sSA == 1)
		hasDefaultSAMRecord.g(g).s(s) = 1;
	end
	if (sSA > 1)
		hasNonDefaultSAMRecord.g(g).s(s) = 1;
	end
end

% apply rules
for i = 1:dataLength
	g = y(i, 1);
	s = y(i, 2);
	if (y(i, 3) == -1)
		sSA = 1;
	elseif (y(i, 3) == -2)
		sSA = NaN;
	else
		sSA = y(i, 3);
	end
	tTYid = y(i, 4);
	if ~isnan(tTYid)
		tTY = tTY_id(tTYid);
	else
		tTY = NaN;
	end
	lotSamplingRate = 1.0 / y(i, 5);
	
	if (tTY == tTY_Name('PROC') || (tTY ~= tTY_Name('METR') && tTY ~= tTY_Name('MH') && tTY ~= tTY_Name('TEST') && tTY ~= tTY_Name('INSP')))
		for sSA_loopVar = S_SamplingMethods
			f_LotSamp_gssSA.g(g).s(s).sSA(sSA_loopVar) = 0.0;
		end
		f_LotSamp_gssSA.g(g).s(s).sSA(1) = 1.0;
	end
	
	if (tTY == tTY_Name('METR') || tTY == tTY_Name('MH') || tTY == tTY_Name('TEST'))
		if (hasDefaultSAMRecord.g(g).s(s) == 1)
			if (sSA == 1)
				if (isnan(lotSamplingRate))
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = 1;
				else
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = lotSamplingRate;
				end
			end
			for sSA_loopVar = S_SamplingMethods
				if (sSA ~= 1)
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA_loopVar) = 0.0;
				end
			end
		else
			for sSA_loopVar = S_SamplingMethods
				f_LotSamp_gssSA.g(g).s(s).sSA(sSA_loopVar) = 0.0;
			end
			f_LotSamp_gssSA.g(g).s(s).sSA(1) = 1.0;
		end
	end
	
	
	if (tTY == tTY_Name('INSP'))
		if (hasDefaultSAMRecord.g(g).s(s) == 1)
			if (sSA == 1)
				if (isnan(lotSamplingRate))
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = 1;
				else
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = lotSamplingRate;
				end
			end
			for sSA_loopVar = S_SamplingMethods
				if (sSA ~= 1)
					f_LotSamp_gssSA.g(g).s(s).sSA(sSA_loopVar) = 0.0;
				end
			end
		elseif (hasNonDefaultSAMRecord.g(g).s(s) == 1)
			if (isnan(lotSamplingRate))
				f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = 1;
			else
				f_LotSamp_gssSA.g(g).s(s).sSA(sSA) = lotSamplingRate;
			end
			f_LotSamp_gssSA.g(g).s(s).sSA(1) = 0.0;
		else
			for sSA_loopVar = S_SamplingMethods
				f_LotSamp_gssSA.g(g).s(s).sSA(sSA_loopVar) = 0.0;
			end
			f_LotSamp_gssSA.g(g).s(s).sSA(1) = 1.0;
		end
	end
	
end

% validate result

for g = S_Products
	for s = S_Steps_g{g}
		for sSA = S_SamplingMethods
			temp = f_LotSamp_gssSA.g(g).s(s).sSA(sSA);
			if (temp > 1) || (temp < 0)
				err = MException('f_LotSamp:OutOfRange', 'Fraction  must be in [0, 1].');
				throw(err);
			end
		end
	end
end

for g = S_Products
	for s = S_Steps_g{g}
		for sSA = S_SamplingMethods
			temp = f_LotSamp_gssSA.g(g).s(s).sSA(sSA);
			if (sSA > 1) && (temp * f_LotSamp_gssSA.g(g).s(s).sSA(1) > 0)
				err = MException('f_LotSamp:ConflictingValues', 'f_LotSamp for a default and non-default sampling method >0 at the same time.');
				throw(err);
			end
		end
	end
end

end

