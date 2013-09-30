-- drop view NSCTest1View_Tool

CREATE VIEW NSCTest1View_Tool AS
SELECT tv.ToolId AS Id, tv.FactoryToolId AS FacId, hqi.HetQueueNumber AS [HetQ.Id],
	tv.FactoryToolTypeId AS [Type], tv.FactoryToolSubTypeId AS SubType, tv.ToolGroup1, tv.ToolGroup2
FROM ToolView tv
LEFT JOIN (
	SELECT hqt.Tool_Id, hqt.HetQueueNumber
	FROM HetQueueTool hqt WITH (NOLOCK)
	JOIN ProcessBatchView pbv
	ON (hqt.ProcessBatch_Id = pbv.Id and pbv.TYPE = 'CTQ')
) hqi
ON (tv.ToolId = hqi.Tool_Id);

/* 
select * from NSCTest1View_Tool;
*/
