-- drop view ProcessBatchView2

create view ProcessBatchView2 as
select pb.ID, pb.TYPE, pb.STARTTIME, pb.ENDTIME, pb.TNOW,
	DATEDIFF(s, pb.STARTTIME, pb.ENDTIME) AS DurationInSeconds
from ProcessBatch pb with (nolock)


/* 
select * from ProcessBatchView2;
*/
