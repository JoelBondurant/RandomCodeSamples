-- drop view NSCTest1View_Recipe

CREATE VIEW NSCTest1View_Recipe AS
SELECT pv.PDFId, op.FactoryId AS OperationId, tv.FactoryToolId AS ToolId, r.t_ProcAve AS t_ProcAve_gst
FROM ResultsGST r with (nolock)
JOIN ProductView pv
ON (r.PRODUCT_ID = pv.ProductId)
JOIN ProductFlowView pfv
ON (r.PRODUCT_ID = pfv.ProductId)
JOIN Operation op with (nolock)
ON (pfv.OperationId = op.Id)
JOIN ToolView tv
ON (r.TOOL_ID = tv.ToolId)
JOIN ProcessBatchView pbv
ON (pbv.Id = r.PROCESSBATCH_Id and pbv.Type = 'CTQ');

/* 
select * from im..NSCTest1View_Recipe;
*/
