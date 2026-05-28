select
    date_trunc('month', o.purchased_at) as mes,
    count(distinct o.order_id) as total_pedidos,
    round(sum(p.payment_value)::numeric, 2) as receita_total
from raw_staging.stg_orders o
join raw_staging.stg_order_payments p
    on o.order_id = p.order_id
where o.order_status = 'delivered'
group by 1
order by 1