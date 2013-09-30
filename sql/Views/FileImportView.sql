-- drop view FileImportView

create view FileImportView as
select fi.id as FileImportId, datediff(s, fi.TimeReceived, isnull(fi.TimeFinished,getdate())) as Duration,
	fi.IsValid, fi.Status, s.StageType as Stage, p.Name as Pipeline, fi.FileName, 
	fi.FileSizeInBytes, fi.TimeReceived, fi.TimeFinished, fi.Md5Hash, fi.InMongo
from fileimport fi with (nolock)
join stage s with (nolock)
on (fi.stage_id = s.id)
join pipeline p with (nolock)
on (fi.pipeline_id = p.id);

/* 
select * from FileImportView;
*/