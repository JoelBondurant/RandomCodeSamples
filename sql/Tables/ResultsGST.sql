-- drop table ResultsGST;

create table ResultsGST (
	ID INT IDENTITY(1, 1),
	PROCESSBATCH_ID NUMERIC(19, 0) NOT NULL,
	PRODUCT_ID NUMERIC(19, 0) NOT NULL,
	STEP_ID NUMERIC(19, 0) NOT NULL,
	TOOL_ID NUMERIC(19, 0) NOT NULL,
	t_ProcAve FLOAT,
	PRIMARY KEY CLUSTERED (ID)
);


ALTER TABLE ResultsGST WITH CHECK ADD CONSTRAINT FK_RESULTSGST_PRODUCT_ID FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT (ID);
ALTER TABLE ResultsGST WITH CHECK ADD CONSTRAINT FK_RESULTSGST_STEP_ID FOREIGN KEY (STEP_ID) REFERENCES STEP (ID);
ALTER TABLE ResultsGST WITH CHECK ADD CONSTRAINT FK_RESULTSGST_PROCESSBATCH_ID FOREIGN KEY (PROCESSBATCH_ID) REFERENCES PROCESSBATCH (ID);
ALTER TABLE ResultsGST WITH CHECK ADD CONSTRAINT FK_RESULTSGST_TOOL_ID FOREIGN KEY (TOOL_ID) REFERENCES TOOL (ID);


-- select * from im..ResultsGST
