-- drop table ResultsGSSSA;

create table ResultsGSSSA (
	ID INT IDENTITY(1, 1),
	PROCESSBATCH_ID NUMERIC(19, 0) NOT NULL,
	PRODUCT_ID NUMERIC(19, 0) NOT NULL,
	STEP_ID NUMERIC(19, 0) NOT NULL,
	SAMPLINGMETHOD_ID NUMERIC(19, 0) NOT NULL,
	f_AcLotSamp FLOAT,
	f_AcWafSamp FLOAT,
	f_AcWafLotSamp FLOAT,
	PRIMARY KEY CLUSTERED (ID)
);


ALTER TABLE ResultsGSSSA WITH CHECK ADD CONSTRAINT FK_RESULTSGSSSA_PRODUCT_ID FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT (ID);
ALTER TABLE ResultsGSSSA WITH CHECK ADD CONSTRAINT FK_RESULTSGSSSA_STEP_ID FOREIGN KEY (STEP_ID) REFERENCES STEP (ID);
ALTER TABLE ResultsGSSSA WITH CHECK ADD CONSTRAINT FK_RESULTSGSSSA_SAMPLINGMETHOD_ID FOREIGN KEY (SAMPLINGMETHOD_ID) REFERENCES SAMPLINGMETHOD (ID);
ALTER TABLE ResultsGSSSA WITH CHECK ADD CONSTRAINT FK_RESULTSGSSSA_PROCESSBATCH_ID FOREIGN KEY (PROCESSBATCH_ID) REFERENCES PROCESSBATCH (ID);

-- select * from im..ResultsGSSSA
