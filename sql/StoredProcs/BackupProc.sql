-- DROP PROCEDURE BackupProc

CREATE PROCEDURE BackupProc

AS

BACKUP DATABASE im
   READ_WRITE_FILEGROUPS
   TO DISK = 'G:\SQL\Backup\im.bak'


/*
exec BackupProc
*/