select
    order_id,
    customer_id,
    order_status,
    order_purchase_timestamp::timestamp as purchased_at,
    order_delivered_customer_date::timestamp as delivered_at,
    order_estimated_delivery_date::timestamp as estimated_delivery_at
from raw.orders
where order_id is not null