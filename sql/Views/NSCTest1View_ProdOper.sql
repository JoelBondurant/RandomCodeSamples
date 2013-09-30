-- drop view NSCTest1View_ProdOper

CREATE VIEW NSCTest1View_ProdOper AS
SELECT pb.tnow AS ResultDateTime, pv.PDFId, op.FactoryId AS OperationId,
	r.f_Load AS f_Load_gs, r.f_Mix AS f_Mix_gs, r.f_LotSamp AS f_LotSamp_gs,
	r.f_OptLotSamp AS f_OptLotSamp_gs, r.t_CTAve AS t_CTAve_gs
FROM ResultsGS r with (nolock)
JOIN ProductView pv
ON (r.PRODUCT_ID = pv.ProductId)
JOIN ProductFlowView pfv
ON (r.PRODUCT_ID = pfv.ProductId and r.step_id = pfv.stepid)
JOIN Operation op with (nolock)
ON (pfv.OperationId = op.Id)
JOIN ProcessBatch pb with (nolock)
ON (r.PROCESSBATCH_Id = pb.Id);


/* 
select * from im..NSCTest1View_ProdOper;
*/
