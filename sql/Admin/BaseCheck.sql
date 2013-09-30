select * from imDev..FileImportView with (nolock)
select * from imDev..LotEventStatistics with (nolock)
select * from imDev..ProcessBatch with (nolock)

select * from imDev..LOGRECORD where LEVEL = 'SEVERE'

select top 100 * from imDev..LotEvent where FILEIMPORTID = 14490333

select top 100 * from imDev..LotMeasurementEvent where FILEIMPORTID = 14490335