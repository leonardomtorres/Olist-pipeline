select
    c.state as estado,
    count(distinct o.order_id) as total_pedidos,
    round(avg(p.payment_value)::numeric, 2) as ticket_medio,
    round(sum(p.payment_value)::numeric, 2) as receita_total
from raw_staging.stg_orders o
join raw_staging.stg_customers c
    on o.customer_id = c.customer_id
join raw_staging.stg_order_payments p
    on o.order_id = p.order_id
where o.order_status = 'delivered'
group by 1
order by 3 desc