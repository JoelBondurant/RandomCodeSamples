-- drop view HistSampMethProdStepStatsView

create view HistSampMethProdStepStatsView as
select h.Product_Id as ProductId, h.Step_Id as StepId, h.SamplingMethod_Id as SamplingMethodId,
	td.DateAndTime, datediff(d, td.dateandtime, pbv.tNow) as p,
	h.n_AllPotWafArr, h.n_LotArr, h.n_PotLotArr, h.n_PotWafArr, h.n_WafArr
from HistSampMethProdStepStats h with (nolock)
join TemporalDate td with (nolock)
on (h.temporaldate_id = td.id)
join ProcessBatchView pbv on ([Type] = 'RTS');


/* 
select * from HistSampMethProdStepStatsView;
*/