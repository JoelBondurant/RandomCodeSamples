-- DROP FUNCTION IMStatus

CREATE FUNCTION IMStatus()
RETURNS @Results TABLE (FileFeedStatus INT, FileImportStatus INT, RTSStatus INT, CTQStatus INT)
AS
BEGIN
/*
Status = 0 <=> Failure
Status = 1 <=> No Failure
*/

-- File feed status:
-- File feed is up is at least one file received in the past half hour.
DECLARE @FileFeedStatus INT;
SELECT @FileFeedStatus = (CASE WHEN a.NumberOfFilesReceived > 0 THEN 1 ELSE 0 END)
FROM (
	SELECT COUNT(1) AS NumberOfFilesReceived
	FROM FileImport fi WITH (NOLOCK)
	WHERE fi.TIMERECEIVED > DATEADD(MINUTE, -30, GETDATE())
) a

-- File import status:
-- File feed has problems if at least one failure occurred in the past three hours.
DECLARE @FileImportStatus INT;
SELECT @FileImportStatus = (CASE WHEN a.NumberOfFilesUnsuccessfullyProcessed > 0 THEN 0 ELSE 1 END)
FROM (
	SELECT COUNT(1) AS NumberOfFilesUnsuccessfullyProcessed
	FROM FileImport fi WITH (NOLOCK)
	WHERE fi.TIMERECEIVED > DATEADD(MINUTE, -180, GETDATE())
	AND fi.STATUS <> 'SUCCESS'
) a

-- RTS status:
-- RTS is working if it has finished within the past half hour.
DECLARE @RTSStatus INT;
SELECT @RTSStatus = (CASE WHEN a.RecentRTSRuns > 0 THEN 1 ELSE 0 END)
FROM (
	SELECT COUNT(1) AS RecentRTSRuns
	FROM LogRecord WITH (NOLOCK)
	WHERE Zone = 'CENTRAL_CONTROL'
	AND MESSAGE = 'RTS finished.'
	AND TimeEntered > DATEADD(MINUTE, -30, GETDATE())
) a

-- CTQ status:
-- CTQ is working if it has finished within the past 12 hours.
DECLARE @CTQStatus INT;
SELECT @CTQStatus = (CASE WHEN a.RecentRTSRuns > 0 THEN 1 ELSE 0 END)
FROM (
	SELECT COUNT(1) AS RecentRTSRuns
	FROM LogRecord WITH (NOLOCK)
	WHERE Zone = 'CENTRAL_CONTROL'
	AND MESSAGE = 'CTQ finished.'
	AND TimeEntered > DATEADD(HOUR, -12, GETDATE())
) a


INSERT @Results
SELECT
@FileFeedStatus AS FileFeedStatus, 
@FileImportStatus AS FileImportStatus,
@RTSStatus AS RTSStatus,
@CTQStatus AS CTQStatus

RETURN;
END;

/* 
SELECT * FROM IMStatus();
*/

