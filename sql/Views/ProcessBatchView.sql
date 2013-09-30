-- drop view ProcessBatchView

create view ProcessBatchView as
select pb.*
from ProcessBatch pb with (nolock)
join (
	select max(id) as MaxId, [Type]
	from ProcessBatch with (nolock)
	group by [Type]
) pbKey
on (pb.id = pbKey.MaxId)

/* 
select * from ProcessBatchView;
*/
