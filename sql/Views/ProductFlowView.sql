-- drop view ProductFlowView

create view ProductFlowView as
select p.id as ProductId, (fs.flow_order + 1) as StepNumber,
	s.id as StepId, s.Operation_Id as OperationId, s.Route_Id as RouteId
from Product p with (nolock)
join Flow f with (nolock)
on (p.id = f.product_id)
join Flow_Step fs with (nolock)
on (f.id = fs.flow_id)
join Step s with (nolock)
on (s.id = fs.steps_id);


/* 
select * from ProductFlowView;
*/