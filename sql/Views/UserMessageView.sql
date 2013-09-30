
-- drop view UserMessageView

create view UserMessageView as
SELECT TOP 30 [TimeEntered], [Message], [Level]
from LOGRECORD WITH (NOLOCK)
WHERE Zone = 'USER'
ORDER BY TimeEntered DESC


/* 
select * from UserMessageView;
*/