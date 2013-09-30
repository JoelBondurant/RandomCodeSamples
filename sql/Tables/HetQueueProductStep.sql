-- drop table HetQueueProductStep;

create table HetQueueProductStep (
	ID INT IDENTITY(1, 1),
	PROCESSBATCH_ID NUMERIC(19, 0) NOT NULL,
	HetQueueNumber INT NOT NULL,
	PRODUCT_ID NUMERIC(19, 0) NOT NULL,
	STEP_ID NUMERIC(19, 0) NOT NULL,
	PRIMARY KEY CLUSTERED (ID)
);


ALTER TABLE HetQueueProductStep WITH CHECK ADD CONSTRAINT FK_HETQPRODUCTSTEP_PRODUCT_ID FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT (ID);
ALTER TABLE HetQueueProductStep WITH CHECK ADD CONSTRAINT FK_HETQPRODUCTSTEP_STEP_ID FOREIGN KEY (STEP_ID) REFERENCES STEP (ID);
ALTER TABLE HetQueueProductStep WITH CHECK ADD CONSTRAINT FK_HETQPRODUCTSTEP_PROCESSBATCH_ID FOREIGN KEY (PROCESSBATCH_ID) REFERENCES PROCESSBATCH (ID);

