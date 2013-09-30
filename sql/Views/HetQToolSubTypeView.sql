-- drop view HetQToolSubTypeView

CREATE VIEW HetQToolSubTypeView AS
SELECT ProcessBatchId, HetQueueNumber, MIN(ToolSubType) AS ToolSubType
FROM (
	SELECT DISTINCT pb.Id AS ProcessBatchId, hqps.HetQueueNumber, tst.FactoryId AS ToolSubType
	FROM ProcessBatch pb with (nolock)
	JOIN ResultsGSF r with (nolock)
	ON (pb.id = r.processbatch_id)
	JOIN ProductView pv
	ON (r.product_id = pv.ProductId)
	JOIN ProductFlowView pfv
	ON (r.product_id = pfv.ProductId AND r.step_id = pfv.StepId)
	JOIN Operation op with (nolock)
	ON (pfv.OperationId = op.id)
	JOIN HetQueueProductStep hqps with (nolock)
	ON (hqps.processbatch_id = pb.id AND r.product_id = hqps.product_id AND r.step_id = hqps.step_id)
	JOIN ResultsQ rq with (nolock)
	ON (pb.id = rq.processbatch_id AND rq.HetQueueNumber = hqps.HetQueueNumber)
	JOIN ToolSubType tst with (nolock)
	ON (op.toolsubtype_id = tst.id)
) a
GROUP BY ProcessBatchId, HetQueueNumber;


/* 
select * from HetQToolSubTypeView;
*/
