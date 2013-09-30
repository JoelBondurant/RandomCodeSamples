-- drop view HistToolProdStepStatsView

create view HistToolProdStepStatsView as
select h.Product_Id as ProductId, h.Step_Id as StepId, h.Tool_Id as ToolId,
	td.DateAndTime, datediff(d, td.dateandtime, pbv.tNow) as p,
	h.n_LotProcCompl, h.t_LotProc, h.n_LotStepCompl, h.t_LotCT
from HistToolProdStepStats h with (nolock)
join TemporalDate td with (nolock)
on (h.temporaldate_id = td.id)
join ProcessBatchView pbv on ([Type] = 'RTS');

/* 
select * from HistToolProdStepStatsView;
*/