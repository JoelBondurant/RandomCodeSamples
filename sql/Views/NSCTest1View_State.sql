-- drop view NSCTest1View_State

CREATE VIEW NSCTest1View_State AS
SELECT pb.tNow AS ResultDateTime, ts.FactoryId AS FacId, 
	t.FactoryId AS [Tool.FacId], r.f_InState AS f_InState_tz
FROM ProcessBatch pb with (nolock)
JOIN ResultsTZ r with (nolock)
ON (pb.id = r.processbatch_id) -- and pbv.TYPE = 'CTQ')
JOIN Tool t with (nolock)
ON (r.tool_id = t.id)
JOIN ToolState ts with (nolock)
ON (r.toolstate_id = ts.id);


/* 
select * from NSCTest1View_State;
*/
