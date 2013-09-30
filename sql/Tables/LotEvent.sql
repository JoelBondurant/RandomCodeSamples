create index Idx_LotEvent_DateAndTime on LotEvent (DateAndTime);

create index Idx_LotEvent_LotId on LotEvent (Lot_Id);

create index Idx_LotEvent_LotId on LotEvent (FILEIMPORTID);
