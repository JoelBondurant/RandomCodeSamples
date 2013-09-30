-- DROP PROCEDURE LotWipDataProc

CREATE PROCEDURE LotWipDataProc

AS


	SELECT lot.Id AS LotId, tool.FactoryId AS FactoryToolId, wc.NumWafers
	INTO #LotBaseData
	FROM Lot lot 
	JOIN ( 
		SELECT LotId, COUNT(1) AS NumWafers 
		FROM WipAlgoWaferView 
		GROUP BY LotId) wc 
	ON (lot.Id = wc.LotId) 
	LEFT JOIN Tool tool 
	ON (lot.Tool_Id = tool.Id);
	
	SELECT lot.Id AS LotId, aop.FactoryId AS ActualFactoryOperationId, apv.PDFId AS ActualPDFId, 
		wop.FactoryId AS WipAlgoFactoryOperationId, wpv.PDFId AS WipAlgoPDFId, 
		opv.PDFId AS OriginalPDFId, waf.WipAlgoProcessingState, 
		RANK() OVER (PARTITION BY waf.LotId ORDER BY waf.WipAlgoProcessingState ASC, waf.WaferId ASC) AS Rnk
	INTO #WaferInfo
	FROM WipAlgoWaferView waf 
	JOIN Operation aop
	ON (waf.ActualOperationId = aop.Id) 
	JOIN ProductView apv 
	ON (waf.ActualProductId = apv.ProductId)
	JOIN Operation wop
	ON (waf.WipAlgoOperationId = wop.Id) 
	JOIN ProductView wpv 
	ON (waf.WipAlgoProductId = wpv.ProductId)
	JOIN ProductView opv 
	ON (waf.WipAlgoProductId = opv.ProductId)
	JOIN Lot lot 
	ON (waf.LotId = lot.Id);

	SELECT LotBaseData.LotId, LotBaseData.FactoryToolId, LotBaseData.NumWafers, 
		LotLocation.ActualFactoryOperationId, LotLocation.ActualPDFId,
		LotLocation.WipAlgoFactoryOperationId, LotLocation.WipAlgoPDFId,
		LotLocation.OriginalPDFId, LotLocation.WipAlgoProcessingState 
	FROM #LotBaseData LotBaseData
	JOIN
	(
		SELECT wi.LotId, wi.ActualFactoryOperationId, wi.ActualPDFId, wi.WipAlgoFactoryOperationId,
			wi.WipAlgoPDFId, wi.OriginalPDFId, wi.WipAlgoProcessingState 
		FROM (
			SELECT *
			FROM #WaferInfo
		) wi 
		WHERE wi.Rnk = 1
	) LotLocation 
	ON (LotBaseData.LotId = LotLocation.LotId)

/*
exec LotWipDataProc
*/