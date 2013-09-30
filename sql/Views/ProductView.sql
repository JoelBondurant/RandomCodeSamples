-- drop view ProductView

create view ProductView as
select p.Id as ProductId, p.factoryid as FactoryProductId, p.UseCode,
	d.id as DeviceId, d.FactoryId as FactoryDeviceId, pf.id as ProductFamilyId,
	pf.factoryid as FactoryProductFamilyId, 
	p.factoryid + '_' + d.factoryid + '_' + pf.factoryid as PDFId
from Product p with (nolock)
join Device d with (nolock)
on (p.device_id = d.id)
join ProductFamily pf with (nolock)
on (d.productfamily_id = pf.id);

/* 
select * from ProductView;
*/