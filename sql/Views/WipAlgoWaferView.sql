-- drop view WipAlgoWaferView

-- declare @timeFilter int;
-- set @timeFilter = 6;

create view WipAlgoWaferView as
select w.Id as WaferId, w.Lot_Id as LotId, w.FactoryId as FactoryWaferId, 
	w.WipAlgoProduct_Id as WipAlgoProductId, w.WipAlgoOperation_Id as WipAlgoOperationId,
	w.WipAlgoProcessingState, w.ActualProduct_Id as ActualProductId, 
	w.ActualOperation_Id as ActualOperationId, w.SamplingMethod_Id as SamplingMethodId
from Wafer w with (nolock)
join ProcessBatchView pbv
on (pbv.TYPE = 'CTQ')
join EventInfo ei with (nolock)
on (w.CurrentEvent_Id = ei.Id)
join Lot lt with (nolock)
on (lt.Id = w.Lot_Id)
where ei.DateAndTime is not null
and ei.DateAndTime > DATEADD(d,-6,pbv.tNow)
and lt.IsFinished = 0
and w.IsActive = 1 -- ?
and w.WipAlgoOperation_Id is not null;

/* 
select * from WipAlgoWaferView;
*/
