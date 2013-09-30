-- drop view WipAlgoWaferView2

create view WipAlgoWaferView2 as
select lot.factoryid as FactoryLotId, wawv.FactoryWaferId, wapv.pdfid as WipAlgoPDFId, waop.factoryid as WipAlgoOperationId,
	 wawv.WipAlgoProcessingState, apv.pdfid as ActualPDFId, aop.factoryid as ActualOperationId, sm.IsDefault
from WipAlgoWaferView wawv
join Lot lot WITH (NOLOCK) on (wawv.lotid = lot.id)
join ProductView wapv on (wawv.wipalgoproductid = wapv.productid)
join Operation waop WITH (NOLOCK) on (wawv.wipalgooperationid = waop.id)
join ProductView apv on (wawv.actualproductid = apv.productid)
join Operation aop WITH (NOLOCK) on (wawv.actualoperationid = aop.id)
join SamplingMethod sm WITH (NOLOCK) on (wawv.samplingmethodid = sm.id);



/* 
select * from WipAlgoWaferView2;
*/
