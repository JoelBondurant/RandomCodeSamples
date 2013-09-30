-- drop view NSCTest1View

CREATE VIEW NSCTest1View AS
SELECT pb.tnow AS ResultDateTime, pv.FactoryProductId AS Product, pv.PDFId AS PDF,
	op.factoryid AS Operation, hqps.HetQueueNumber AS [HetQ.Id], r.ForecastDateTime AS ForecastDateTime, r.ForecastId,
	r.ShiftId AS n_ForecastShiftId_f, r.n_FcWafWIP AS n_FcWafWIP_gsf, r.n_TargWafWIP AS n_TargWafWIP_gsf,
	r.n_FcPotWafWIP AS n_FcPotWafWIP_gsf, r.n_UpTargWafWIP AS n_UpTargWafWIP_gsf,
	r.n_LoTargWafWIP AS n_LoTargWafWIP_gsf
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
ON (hqps.processbatch_id = pb.id AND r.product_id = hqps.product_id AND r.step_id = hqps.step_id);

/* 
select * from NSCTest1View;
*/
