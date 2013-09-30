-- drop view ToolChamberView

create view ToolChamberView as
select tc.id as ToolChamberId, tc.factoryId as FactoryToolChamberId, tv.*
from ToolChamber tc WITH (NOLOCK)
join ToolView tv
on (tc.parentTool_id = tv.toolId);


/* 
select * from ToolChamberView;
*/