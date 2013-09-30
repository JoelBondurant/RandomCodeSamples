-- drop view NSCTest1View_Product

CREATE VIEW NSCTest1View_Product AS
SELECT pv.FactoryProductId AS Product, pv.FactoryDeviceId AS Device, pv.FactoryProductFamilyId AS Family,
	p.UseCode AS ProdUse, pv.PDFId
FROM ProductView pv
JOIN Product p with (nolock)
ON (p.id = pv.productid);

/* 
select * from NSCTest1View_Product;
*/
