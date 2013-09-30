
-- drop view ToolView

create view ToolView as
select t.id as ToolId, t.factoryid as FactoryToolId, ts.id as ToolStateId, ts.factoryid as FactoryToolStateId,
	tst.id as ToolSubTypeId, tst.factoryid as FactoryToolSubTypeId, tt.id as ToolTypeId,
	tt.factoryid as FactoryToolTypeId,  tg1.FACTORYID as ToolGroup1, tg2.FACTORYID as ToolGroup2,
	t.MaxDegreeOfParallelism
from Tool t WITH (NOLOCK)
left join ToolState ts WITH (NOLOCK)
on (ts.id = t.toolstate_id)
left join ToolSubType tst WITH (NOLOCK)
on (tst.id = t.toolsubtype_id)
left join ToolType tt WITH (NOLOCK)
on (tt.id = tst.tooltype_id)
left join ToolGroup1 tg1 WITH (NOLOCK)
on (tg1.ID = t.TOOLGROUP1_ID)
left join ToolGroup2 tg2 WITH (NOLOCK)
on (tg1.TOOLGROUP2_ID = tg2.ID)


/* 
select * from ToolView;
*/