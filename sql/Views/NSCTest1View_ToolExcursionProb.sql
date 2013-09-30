-- drop view NSCTest1View_ToolExcursionProb

CREATE VIEW NSCTest1View_ToolExcursionProb AS
SELECT pb.tNow, tv.FactoryToolId, tv.FactoryToolSubTypeId, tv.FactoryToolTypeId, tv.ToolGroup1, tv.ToolGroup2, tess.p_ExcNS
FROM ToolExcursionStatsSlice tess WITH (NOLOCK)
JOIN ProcessBatch pb WITH (NOLOCK)
ON (tess.PROCESSBATCH_ID = pb.ID)
JOIN ToolView tv
ON (tess.TOOL_ID = tv.ToolId)

/* 
select * from NSCTest1View_ToolExcursionProb;
*/
