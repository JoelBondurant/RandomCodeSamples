-- DROP PROCEDURE LotSamplingMethodsProc

CREATE PROCEDURE LotSamplingMethodsProc

AS

SELECT DISTINCT LotId, SamplingMethodId
FROM WipAlgoWaferView;


/*
exec LotSamplingMethodsProc
*/