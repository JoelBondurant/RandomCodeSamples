-- drop view NSCTest1View_HetQ

CREATE VIEW NSCTest1View_HetQ AS
SELECT pb.tnow AS ResultDateTime, hq.HetQueueNumber AS Id, hq.ToolSubType,
	rq.f_Load AS f_Load_q, rq.f_Mix AS f_Mix_q, rq.f_LxM AS f_LxM_q
FROM ResultsQ rq with (nolock)
JOIN ProcessBatch pb with (nolock)
ON (pb.id = rq.processbatch_id)
JOIN HetQToolSubTypeView hq
ON (rq.HetQueueNumber = hq.HetQueueNumber AND pb.id = hq.ProcessBatchId);


/* 
select * from NSCTest1View_HetQ;
*/
