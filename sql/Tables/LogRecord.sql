-- DROP TABLE LogRecord

CREATE TABLE LogRecord (
	[Level] VARCHAR(16),
	TimeEntered DATETIME,
	[Message] VARCHAR(256),
	[Zone] VARCHAR(64),
	[SourceClass] VARCHAR(64),
	[SourceMethod] VARCHAR(64),
	[HostName] VARCHAR(64),
	[HostAddress] VARCHAR(64),
	[ThreadId] INT
)


create index Idx_LogRecord_Level on LogRecord ([Level]);

create index Idx_LogRecord_TimeEntered on LogRecord (TimeEntered);
