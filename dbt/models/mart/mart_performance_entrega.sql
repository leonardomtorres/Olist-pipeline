select
    c.state as estado,
    count(distinct o.order_id) as total_pedidos,
    count(
        distinct case
            when o.delivered_at > o.estimated_delivery_at
            then o.order_id
        end
    ) as pedidos_atrasados,
    round(
        count(distinct case when o.delivered_at > o.estimated_delivery_at then o.order_id end)::numeric
        / nullif(count(distinct o.order_id), 0) * 100
    , 1) as pct_atraso
from raw_staging.stg_orders o
join raw_staging.stg_customers c
    on o.customer_id = c.customer_id
where o.delivered_at is not null
group by 1
order by 4 desc