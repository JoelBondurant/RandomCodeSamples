-- drop view HistToolStateStatsView

create view HistToolStateStatsView as
select h.Tool_Id as ToolId, h.ToolState_Id as ToolStateId, datediff(d, td.dateandtime, pbv.tNow) as p,
	h.DurationInSeconds, h.FullDurationInSeconds, h.NumStateEndings
from HistToolStateStats h with (nolock)
join TemporalDate td with (nolock)
on (h.temporaldate_id = td.id)
join ProcessBatchView pbv on ([Type] = 'RTS');

/* 
select * from HistToolStateStatsView;
*/