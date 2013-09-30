-- drop table ResultsGS;

create table ResultsGS (
	ID INT IDENTITY(1, 1),
	PROCESSBATCH_ID NUMERIC(19, 0) NOT NULL,
	PRODUCT_ID NUMERIC(19, 0) NOT NULL,
	STEP_ID NUMERIC(19, 0) NOT NULL,
	f_Load FLOAT,
	f_Mix FLOAT,
	f_LotSamp FLOAT,
	f_OptLotSamp FLOAT,
	t_CTAve FLOAT,
	PRIMARY KEY CLUSTERED (ID)
);


ALTER TABLE ResultsGS WITH CHECK ADD CONSTRAINT FK_RESULTSGS_PRODUCT_ID FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT (ID);
ALTER TABLE ResultsGS WITH CHECK ADD CONSTRAINT FK_RESULTSGS_STEP_ID FOREIGN KEY (STEP_ID) REFERENCES STEP (ID);
ALTER TABLE ResultsGS WITH CHECK ADD CONSTRAINT FK_RESULTSGS_PROCESSBATCH_ID FOREIGN KEY (PROCESSBATCH_ID) REFERENCES PROCESSBATCH (ID);

-- select * from im..ResultsGS